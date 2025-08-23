from django.urls import path
from django.contrib.auth import views
from .views import (dashboard, UserLoginView, book_suggestion,
                    see_borrowed_books, see_requests, successful, create_request, check_score,)

urlpatterns = [
    
    # user side
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', dashboard, name='dashboard'),
    path('see_borrowed_books/', see_borrowed_books, name='see_borrowed_books'),
    path('see_requests/', see_requests, name='see_requests'),
    path('create_request/<int:loan_id>', create_request, name='create_request'),
    path('book_suggestion/', book_suggestion, name='book_suggestion'),
    path('check_score/', check_score, name='check_score'),
    path('successful/', successful, name='successful'),

]
