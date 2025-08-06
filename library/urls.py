from django.urls import path
from django.contrib.auth import views
from .views import (import_pdf_file, dashboard, undo_loan,
                    create_user, create_loan, search_books,
                    UserLoginView, admin_see_requests, book_suggestion,
                    admin_dashboard, see_borrowed_books,
                    see_requests, successful, create_request,
                    accepte_request, reject_request, return_score_entry,
                    see_score,
                    )

urlpatterns = [  # Todo: create another path for the admin side
    path("account/login/", views.LoginView.as_view(), name="admin_login"),
    path('admin/import_file/', import_pdf_file, name='import_excle_file'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/undo_return/<int:loan_id>', undo_loan, name='undo_return'),
    path('admin/create_loan/', create_loan, name='create_loan'),
    path('admin/create_user/', create_user, name='create_user'),
    path('admin/search_books/', search_books, name='search_books'),
    path('admin/accepte_request/<int:request_id>',
         accepte_request, name='accepte_request'),
    path('admin/reject_request/<int:request_id>',
         reject_request, name='reject_request'),
    path('admin/see_requests/', admin_see_requests, name='admin_see_requests'),
    path('admin/see_score/', see_score, name='see_score'),
    # user side
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', dashboard, name='dashboard'),
    path('see_borrowed_books/', see_borrowed_books, name='see_borrowed_books'),
    path('see_requests/', see_requests, name='see_requests'),
    path('create_request/<int:loan_id>', create_request, name='create_request'),
    path('book_suggestion/', book_suggestion, name='book_suggestion'),


    path('successful/', successful, name='successful'),
    path('return_score_entry/<int:joined_number>',
         return_score_entry, name='return_score_entry'),



]
