from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now, timedelta
from django.shortcuts import get_object_or_404
from django.http.request import HttpRequest
from account.forms import CustomUserForm
from account.models import CustomUser
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Loan
from datetime import datetime
from .forms import LoanForm
import pandas as pd
import pdfplumber
import threading


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
        code_number = row['code'].split('.')[0].zfill(4)
        code_char = '.'.join(row['code'].split('.')[1:][::-1]).strip()
        code = code_number + \
            code_char if not (code_number == '0000' or code_char == '') else ''
        code = code.replace(' ', '')
        try:
            book = Book.objects.create(
                name=row['name'], code=code,
                row_number=int(row['row_number']))
        except:
            pass


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


@superuser_required
def import_excle_file(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        file = request.FILES["inputfile"]
        t1 = threading.Thread(target=handle_uploaded_file, args=(file,))
        t1.start()
        context['succses'] = True
    return render(request, 'library\inputfile.html', context)


@superuser_required
def dashbord(request: HttpRequest):
    thirty_days_ago = now() - timedelta(days=30)
    thirty_days_ago_loans = Loan.objects.filter(
        return_date__gte=thirty_days_ago)
    thirty_days_ago_loans = [
        thirty_days_ago_loans.filter(is_return=False).count(),
        thirty_days_ago_loans.filter(is_return=True).count()]
    today_date = datetime.now()
    unforce_return = Loan.objects.filter(
        is_return=False)
    force_return = Loan.objects.filter(
        is_return=False, return_date__lte=today_date)
    unforce_return = unforce_return.exclude(
        id__in=force_return.values_list('id', flat=True))

    context = {'force_return': force_return, 'unforce_return': unforce_return,
               'thirty_days_ago_loans': thirty_days_ago_loans}
    return render(request, 'library\dashbord.html', context)


@superuser_required
def create_user(request: HttpRequest):
    form = CustomUserForm()
    context = {'form': form, 'error': None}

    if request.method == 'POST':
        fullname = request.POST['fullname']
        classname = request.POST['classname']
        joined_number = request.POST['joined_number']
        last_id = str(CustomUser.objects.last().id)
        try:
            user = CustomUser.objects.create(

                username=fullname+last_id, fullname=fullname,
                classname=classname, joined_number=joined_number)

            user.set_password(str(int(joined_number)*2+3))
            user.save()
        except BaseException as e:
            context['error'] = 'این شماره عضویت وجود دارد'

    return render(request, 'library\create_user.html', context)


def search(request: HttpRequest):
    input = request.GET.get('input', None)
    books = Book.objects.filter(name__contains=input if input else '')
    if input is None:
        books = books[:20]
    context = {'books': books, 'count': Book.objects.all().count()
               if not input else books.count()}
    return render(request, 'library\search.html', context)


@superuser_required
def create_loan(request: HttpRequest):
    form = LoanForm()
    context = {'form': form, 'errors': []}
    if request.method == 'POST':
        context['form'] = LoanForm(request.POST)
        joined_number = request.POST['joined_number'].replace(' ', '')
        try:
            user = get_object_or_404(CustomUser, joined_number=joined_number)
        except:
            context['errors'].append('این شماره عضویت وجود ندارد')
        book_code = request.POST['book_code'].replace(' ', '')
        try:
            book = get_object_or_404(Book, code=book_code)
        except:
            context['errors'].append('این کد برای کتاب ها وجود ندارد')
        if not context['errors'] == []:
            return render(request, 'library\create_loan.html', context)
        loan_date = request.POST['loan_date'].replace('/', '-')
        return_date = request.POST['return_date'].replace('/', '-')
        notes = request.POST['notes']

        loan = Loan.objects.create(
            user=user, book=book, loan_date=loan_date,
            return_date=return_date, notes=notes)
        loan.save()
    return render(request, 'library\create_loan.html', context)

    context = {'user_loans': None}
    input = request.GET.get('input', None)

    if input:
        user_loans = []
        users = CustomUser.objects.filter(fullname__contains=input)
        for user in users:
            loans = Loan.objects.filter(user=user)
            user_loans.append({user: loans})

        context['user_loans'] = user_loans

    return render(request, 'library\search_user.html', context)


@superuser_required
def undo_loan(request, loan_id: int):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.is_return = True
    loan.save()
    return HttpResponse('all is right')
