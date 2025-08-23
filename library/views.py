from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Case, When, IntegerField, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http.request import HttpRequest
from .models import Book, Loan, Request
from account.models import ScoreEntry
from .utils import *


class UserLoginView(LoginView):
    template_name = 'library/user-side/login.html'
    redirect_authenticated_user = 'dashboard'


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
        user=request.user)
    unreturned_books_count = Loan.objects.filter(
        user=request.user, is_return=False).count()
    context = {"borrowed_books": borrowed_books,
               "unreturned_books_count": unreturned_books_count}
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


@login_required
def check_score(request: HttpRequest):
    user = request.user
    scores = ScoreEntry.objects.filter(user=user)[:10]
    context = {'scores': scores}

    return render(request, 'library/user-side/check_score.html', context)


@login_required
def book_suggestion(request: HttpRequest):
    user = request.user
    avg_embedding = get_user_embedding(user)
    if not isinstance(avg_embedding, bool):
        books = get_similar_books(avg_embedding, user=user)

    else:
        books = Book.objects.annotate(
            loan_count=Count('loan')
        ).order_by(
            '-loan_count')[:5]
    context = {'books': books}

    return render(request, 'library/user-side/book_suggestion.html', context)
