from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Case, When, IntegerField, Sum
from .models import Book, Loan, Category, Post, Request
from account.models import CustomUser, ScoreEntry
from django.contrib.auth.views import LoginView
from .forms import BookSearchForm, PostForm
from django.http.request import HttpRequest
from account.forms import CustomUserForm
from datetime import timedelta, datetime
from django.http import JsonResponse
from .forms import LoanForm
from jdatetime import date
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
def import_pdf_file(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        try:
            file = request.FILES["inputfile"]
            t1 = threading.Thread(target=handle_uploaded_file, args=(file,))
            t1.start()
            context['succses'] = True
        except:
            pass

        try:
            row_number = request.POST["row_number"]
            book_name = request.POST["book_name"]
            book_code = request.POST["book_code"]
            book = Book.objects.create(
                name=book_name, row_number=row_number, code=book_code)
            book.save()
            context['succses'] = True
        except:
            pass

    return render(request, 'library/admin/inputfile.html', context)


@superuser_required
def admin_dashboard(request: HttpRequest):
    today_date = datetime.now()
    print(today_date)
    unforce_return = Loan.objects.filter(
        is_return=False)
    force_return = Loan.objects.filter(
        is_return=False, return_date__lte=today_date)
    unforce_return = unforce_return.exclude(
        id__in=force_return.values_list('id', flat=True))

    context = {'force_return': force_return,
               'unforce_return': unforce_return, }
    return render(request, 'library/admin/dashboard.html', context)


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
            password = str(int(joined_number)*2+3) + \
                str(int(joined_number)*2+CustomUser.objects.last())

            user.set_password(password)
            user.save()
            context['created_user'] = user
            context['pass'] = password
        except BaseException as e:
            context['error'] = 'این شماره عضویت وجود دارد'

    return render(request, 'library/admin/create_user.html', context)


def home_page(request: HttpRequest):
    five_last_posts = Post.objects.all().order_by('-id')[:4]
    five_last_books = Book.objects.all().order_by('-id')[:5]
    context = {'posts': five_last_posts, 'books': five_last_books}
    return render(request, 'library/user-side/homepage.html', context)


def see_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'library/user-side/see_post.html', context)


def see_all_posts(request: HttpRequest):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'library/user-side/see_all_posts.html', context)


def search_book(request: HttpRequest):
    input = request.GET.get('input', None).strip()
    books = Book.objects.filter(name__contains=input if input else '')
    if input is None or input == '':
        books = books[:20]
    context = {'books': books, 'count': Book.objects.all().count()
               if not input else books.count(), 'input': input}

    return render(request, 'library/user-side/search_book.html', context)


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
            return render(request, 'library/admin/create_loan.html', context)
        loan_date = request.POST['loan_date'].replace('/', '-')
        return_date = request.POST['return_date'].replace('/', '-')
        notes = request.POST['notes']

        loan = Loan.objects.create(
            user=user, book=book, loan_date=loan_date,
            return_date=return_date, notes=notes)
        loan.save()
    return render(request, 'library/admin/create_loan.html', context)


@superuser_required
def undo_loan(request: HttpRequest, loan_id: int):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.is_return = True
    today_date = date.today()
    if loan.return_date < today_date:
        score = ScoreEntry.objects.create(
            user=loan.user, score=-1, reason='تحویل دیر کتاب ')
        score.save()
    loan.save()
    return redirect('successful')


@superuser_required
def decrease_score(request: HttpRequest, loan_id: int):
    loan = get_object_or_404(Loan, id=loan_id)
    user = loan.user
    score = ScoreEntry.objects.create(
        user=user, score=-1, reason='به دلیل تحویل دیر وقت')
    loan.is_return = True
    score.save()
    loan.save()
    return redirect('successful')


@superuser_required
def search_books(request: HttpRequest):
    form = BookSearchForm(request.GET or None)
    context = {'form': form}
    results = None
    if form.is_valid():
        name = form.cleaned_data.get('name')
        code = form.cleaned_data.get('code')
        user = form.cleaned_data.get('user')
        is_return = form.cleaned_data.get('is_return')
        results = Loan.objects.select_related('book', 'user')
        if name:
            results = results.filter(book__name__contains=name)
        if code:
            results = results.filter(book__code__contains=code)
        if user:
            results = results.filter(user__username__contains=user)
        if is_return is not None:
            results = results.filter(is_return=is_return)
        context['is_return'] = is_return
        context['results'] = results
    return render(request, 'library/admin/search_books.html', context)


@superuser_required
def admin_see_requests(request: HttpRequest):
    requests = Request.objects.all().filter(status='processing')
    context = {}
    context['requests'] = requests
    return render(request, 'library/admin/see_requests.html', context)


@superuser_required
def accepte_request(request: HttpRequest, request_id: int):
    request: Request = get_object_or_404(Request, id=request_id)
    loan = request.loan
    loan.have_request = True
    loan.return_date = loan.return_date + timedelta(days=7)
    loan.save()
    request.status = 'accepted'
    request.save()
    return redirect('successful')


@superuser_required
def reject_request(request: HttpRequest, request_id: int):
    request: Request = get_object_or_404(Request, id=request_id)
    request.status = 'rejected'
    request.save()
    return redirect('successful')


class UserLoginView(LoginView):
    template_name = 'library/user-side/login.html'
    redirect_authenticated_user = 'homepage'


@superuser_required
def create_post(request: HttpRequest):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'library/admin/create_post.html', context)


@superuser_required
def edit_post(request: HttpRequest, post_id):

    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.data
            post.title = data['title']
            post.body = data['body']
            post.categories.clear()
            for i in request.POST.getlist('categories'):
                category = Category.objects.get(id=i)
                post.categories.add(category)
            post.save()

    title_value = post.title
    body_value = post.body
    context = {'form': form,
               'title_value': title_value, 'body_value': body_value}
    return render(request, 'library/admin/edit_post.html', context)


@superuser_required
def see_posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'library/admin/see_posts.html', context)


@superuser_required
def create_category(request: HttpRequest):
    if request.method == "POST":
        name = request.POST['name']
        category = Category.objects.create(name=name)
        category.save()
    context = {}
    return render(request, 'library/admin/create_category.html', context)


@login_required
def dashboard(request: HttpRequest):
    borrowed_books = Loan.objects.filter(
        user=request.user).count()
    unreturned_books_list = Loan.objects.filter(
        user=request.user, is_return=False)
    context = {"borrowed_books": borrowed_books,
               "unreturned_books_list": unreturned_books_list}
    return render(request, 'library/user-side/dashboard.html', context)


@login_required
def see_borrowed_books(request: HttpRequest):
    borrowed_books = Loan.objects.filter(
        user=request.user).count()
    unreturned_books_list = Loan.objects.filter(
        user=request.user, is_return=False)
    context = {"borrowed_books": borrowed_books,
               "unreturned_books_list": unreturned_books_list}
    return render(request, 'library/user-side/see_borrowed_books.html', context)


@login_required
def see_requests(request: HttpRequest):
    requests = Request.objects.annotate(
        custom_order=Case(
            When(status='processing', then=0),
            When(status='accepted', then=1),
            When(status='rejected', then=2),
            output_field=IntegerField(),
        )
    ).order_by('custom_order', 'status')

    processing_requests = requests.filter(status='processing').count()
    accepted_requests = requests.filter(status='accepted').count()
    unaccepted_requests = requests.filter(status='rejected').count()

    requests = requests[:10]
    context = {
        'requests': requests,
        'processing_requests': processing_requests,
        'accepted_requests': accepted_requests,
        'unaccepted_requests': unaccepted_requests,
    }
    return render(request, 'library/user-side/see_requests.html', context)


def successful(request: HttpRequest):
    context = {}
    return render(request, 'successful.html', context)


@login_required
def create_request(http_request: HttpRequest, loan_id: int = None):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.have_request = True
    loan.save()
    request = Request.objects.create(loan=loan)
    request.save()
    return redirect('successful')


def return_score_entry(request: HttpRequest, joined_number: int = None):
    user: CustomUser = get_object_or_404(
        CustomUser, joined_number=joined_number)
    score_entries = user.score_entries.all().values(
        'id', 'score', 'reason', 'date', 'user_id')
    total_score = user.score_entries.aggregate(Sum('score'))['score__sum'] or 0

    data = list(score_entries).append(total_score)
    return JsonResponse(data, safe=False)
