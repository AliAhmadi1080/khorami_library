from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from account.models import CustomUser
from library.models import Book,Loan
from django.db.models import Count
from django.conf import settings
from datetime import datetime
from openai import OpenAI
from os import environ
import pandas as pd
import pdfplumber
import json

token = environ.get('GITHUB_TOKEN')
endpoint = "https://api.groq.com/openai/v1"
model = "openai/gpt-oss-20b"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


def getUserInfo(joined_number: int):
    user = CustomUser.objects.get(joined_number=joined_number)
    if user.DoesNotExist:
        return 'کاربر مورد نظر شما پیدا نشد.'

    loans = Loan.objects.filter(user=user)
    current_loans = [{"book_name": loan.book.name, "loan_date": loan.date} for loan in loans]

    return {
        "joined_number": joined_number,
        "user_name": user.fullname,
        "current_loans": current_loans,
        "total_loans": loans.count()
    }

def getMostPopularBooks(limit: int = 5):
    books_with_loans = Book.objects.annotate(
    loan_count=Count('loan')  
).order_by('-loan_count')[:limit]
    books_with_popularity = [
        {"name": book.name, "code": book.code, "popularity": Loan.objects.filter(book=book).count()}
        for book in books_with_loans
    ]
    return books_with_popularity

def getLibraryGeneralInfo():
    total_members = CustomUser.objects.count()
    total_books = Book.objects.count()
    total_loans = Loan.objects.count()

    return {
        "total_members": total_members,
        "total_books": total_books,
        "total_loans": total_loans,
    }

def getOverdueLoans():
    today_date = datetime.now()
    force_return = Loan.objects.filter(
        is_return=False, return_date__lte=today_date)
    result = []
    for loan in force_return:
        result.append({
            "book_name": loan.book.name,
            "member_name": loan.user.fullname,
            "return_date": loan.return_date
        })
    return result


def get_book_general_info(name: str = None, code: str = None):
    if name is None and code is None:
        return 'کتابی با این مشخصات پیدا نشد'

    books = Book.objects.all()
    if name:
        books = books.filter(name__icontains=name)
    if code:
        books = books.filter(code__icontains=code)

    if not books.exists():
        return 'کتابی پیدا نشد'

    for book in books:
        book.popularity = Loan.objects.filter(book=book).count()

    return {'نام کتاب':books[0].name, "میزان محبوبیت":books[0].popularity, "کد کتاب":books[0].code}



def get_ai_response(history: list[dict]):
    # مرحله اول: مدل رو صدا می‌زنیم
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": settings.AI_SYSTEM_PROMPT}, *history],
        temperature=1.0,
        top_p=1.0,
        tools=settings.TOOLS,
    )

    message = response.choices[0].message
    results = []
    if message.tool_calls is None:
        return response.choices[0].message.content
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        
        if tool_call.function.name == "get_book_general_info":
            result = get_book_general_info(**args)
        elif tool_call.function.name == "getLibraryGeneralInfo":
            result = getLibraryGeneralInfo()
        elif tool_call.function.name == "getMostPopularBooks":
            result = getMostPopularBooks()
        elif tool_call.function.name == "getUserInfo":
            result = getUserInfo(**args)
        elif tool_call.function.name == "getOverdueLoans":
            result = getOverdueLoans()
        else:
            result = "ابزاری یافت نشد"

        # اضافه کردن خروجی tool به مدل برای ادامه مکالمه
        results.append({"tool_call_id": tool_call.id, "result": result})

        # مرحله دوم: دوباره مدل رو صدا می‌زنیم و نتیجه tool رو پاس می‌دیم
        final_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": settings.AI_SYSTEM_PROMPT},
                *history,
                message,
                {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)},
            ],
        )

        return final_response.choices[0].message.content

    # اگر ابزار لازم نبود
    return message.content
def superuser_required(function=None, redirect_field_name='next', login_url='/account/login/'):
    """
    Decorator for views that checks that the user is a superuser, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def handle_uploaded_file(f):
    with open("files/name.pdf", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    pdf_path = 'files/name.pdf'
    rows_list = []
    Book.objects.all().delete()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    numbetsdone = 0
                    text = ''
                    for char in row[1][::-1]:
                        if not char.isdigit():
                            text += char
                            numbetsdone = 0
                        else:
                            if numbetsdone == 0:
                                text += char
                                numbetsdone += 1
                            else:
                                text = text[:-1 * numbetsdone] + \
                                    char + text[-1 * numbetsdone:]
                                numbetsdone += 1
                    row[1] = text
                    rows_list.append(row)

    df = pd.DataFrame(rows_list[1:], columns=rows_list[0])
    df.columns = ['code', "name", 'row_number']
    for index, row in df.iterrows():
        code_number = row['code'].split('.')[0].zfill(4).strip()

        code_char = '.'.join(row['code'].split('.')[1:][::-1]).strip()

        code = code_number + \
            code_char if not (code_number == '0000'
                              or code_char == '') else ''
        code = code.replace(' ', '').strip()

        if code == '' or row['name'] == '':
            continue
        try:
            book = Book.objects.create(
                name=row['name'], code=code,
                row_number=int(row['row_number']))
            book.save()
        except:
            pass
    call_command('generate_embedding')
