from django.http.response import (HttpResponseNotAllowed,
                                  JsonResponse, HttpResponseBadRequest)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from library.forms import LoanForm, BookSearchForm
from account.models import CustomUser, ScoreEntry
from django.core.management import call_command
from library.models import Book, Loan, Request
from django.http.request import HttpRequest
from account.forms import CustomUserForm
from datetime import timedelta, datetime
from django.db.models import Q
from jdatetime import date
from json import loads
from .utils import *
import threading

@superuser_required
def import_pdf_file(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        try:
            file = request.FILES["inputfile"]
            t1 = threading.Thread(target=handle_uploaded_file, args=(file,))
            t1.start()
            context['succses'] = True
            call_command('generate_embedding')
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
            call_command('generate_embedding')
        except:
            pass

    return render(request, 'library/admin/inputfile.html', context)


@superuser_required
def admin_dashboard(request: HttpRequest):
    today_date = datetime.now()
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
                str(int(joined_number)*2+CustomUser.objects.last().id)

            user.set_password(password)
            user.save()
            context['created_user'] = user
            context['pass'] = password
        except BaseException as e:
            context['error'] = 'این شماره عضویت وجود دارد'

    return render(request, 'library/admin/create_user.html', context)


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
            user=loan.user, score=-1, reason='تحویل دیر کتاب: '+loan.book.name[:40]+'...')
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
        user = request.user
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
def see_score(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        fullname = request.POST['full_name'].strip()
        try:
            joined_number = int(request.POST['joined_number'].strip())
        except:
            joined_number = None

        if fullname or joined_number:
            users = CustomUser.objects.filter(
                Q(fullname=fullname) | Q(joined_number=joined_number))
            context['users'] = users

    return render(request, 'library/admin/see_scores.html', context)


@superuser_required
def user_score(request: HttpRequest, joined_number: int):
    user = get_object_or_404(CustomUser, joined_number=joined_number)
    scores = ScoreEntry.objects.filter(user=user)[:15]
    context = {'user': user, 'scores': scores}
    if request.method == 'POST':
        try:
            score = request.POST['score']
            reason = request.POST['reason']
            scoreentry = ScoreEntry.objects.create(
                user=user, score=score, reason=reason)
            scoreentry.save()
            context['succses'] = True
        except:
            context['succses'] = 'false'

    return render(request, 'library/admin/user_score.html', context)


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


@superuser_required
def chat(request: HttpRequest):
    context = {}
    return render(request, 'library/admin/chat.html', context)

@csrf_exempt
@superuser_required
def chat_api(request: HttpRequest):
    if request.method == 'POST':
        post = loads(request.body.decode())
        try:
            history = post['history']  # لیست پیام‌های user و assistant
        except:
            return HttpResponseBadRequest('send history in json')

        # حالا باید get_ai_response بتونه history رو هندل کنه
        response = get_ai_response(history)

        return JsonResponse({'response': response})
    else:
        return HttpResponseNotAllowed(['POST', 'OPTION'])


