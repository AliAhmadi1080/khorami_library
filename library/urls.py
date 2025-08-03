from django.urls import path
from django.contrib.auth import views
from .views import (import_pdf_file, dashboard, undo_loan,
                    home_page, create_user, create_loan, search_books,
                    UserLoginView, search_book, create_post,
                    create_category, see_posts, edit_post,
                    see_post, see_all_posts, admin_dashboard, see_borrowed_books,
                    see_requests, successful, create_request, admin_see_requests,
                    accepte_request, reject_request, return_score_entry
                    )

urlpatterns = [  # Todo: create another path for the admin side
    path("account/login/", views.LoginView.as_view(), name="admin_login"),
    path('admin/import_file/', import_pdf_file, name='import_excle_file'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/create_post/', create_post, name='create_post'),
    path('admin/undo_return/<int:loan_id>', undo_loan, name='undo_return'),
    path('admin/create_loan/', create_loan, name='create_loan'),
    path('admin/create_user/', create_user, name='create_user'),
    path('admin/search_books/', search_books, name='search_books'),
    path('admin/create_category/', create_category, name='create_category'),
    path('admin/see_posts/', see_posts, name='see_posts'),
    path('admin/edit_post/<int:post_id>', edit_post, name='edit_post'),
    path('admin/accepte_request/<int:request_id>',
         accepte_request, name='accepte_request'),
    path('admin/reject_request/<int:request_id>',
         reject_request, name='reject_request'),
    path('admin/edit_post/<int:post_id>', edit_post, name='edit_post'),
    path('admin/see_requests/', admin_see_requests, name='admin_see_requests'),
    # user side
    path('', home_page, name='homepage'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('see_post/<int:post_id>', see_post, name='see_post'),
    path('see_all_posts/', see_all_posts, name='see_all_posts'),
    path('search_book/', search_book, name='search_book'),
    path('dashboard/', dashboard, name='dashboard'),
    path('see_borrowed_books/', see_borrowed_books, name='see_borrowed_books'),
    path('see_requests/', see_requests, name='see_requests'),
    path('create_request/<int:loan_id>', create_request, name='create_request'),

    path('successful/', successful, name='successful'),
    path('return_score_entry/<int:joined_number>',
         return_score_entry, name='return_score_entry'),


]
