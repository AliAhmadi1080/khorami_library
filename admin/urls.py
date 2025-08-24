from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path("account/login/", views.LoginView.as_view(), name="admin_login"),
    path('import_file/', import_pdf_file, name='import_excle_file'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('undo_return/<int:loan_id>', undo_loan, name='undo_return'),
    path('create_loan/', create_loan, name='create_loan'),
    path('create_user/', create_user, name='create_user'),
    path('search_books/', search_books, name='search_books'),
    path('accepte_request/<int:request_id>',
         accepte_request, name='accepte_request'),
    path('reject_request/<int:request_id>',
         reject_request, name='reject_request'),
    path('see_requests/', admin_see_requests, name='admin_see_requests'),
    path('see_score/', see_score, name='see_score'),
    path('user_score/<int:joined_number>/', user_score, name='user_score'),
    path('chat', chat, name='chat'),
    path('chat/api', chat_api, name='chat_api'),
]
