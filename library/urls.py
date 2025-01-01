from django.urls import path
from django.contrib.auth import views
from .views import (import_pdf_file, dashbord, undo_loan,
                    home_page, create_user, create_loan, search_books,
                    UserLoginView, search_book, create_post, create_category,
                    see_posts, edit_post,
                    )

urlpatterns = [
    path("account/login/", views.LoginView.as_view(), name="admin_login"),
    path('import_file/', import_pdf_file, name='import_excle_file'),
    path('dashbord/', dashbord, name='dashbord'),
    path('create_post/', create_post, name='create_post'),
    path('undo_return/<int:loan_id>', undo_loan, name='undo_return'),
    path('create_loan/', create_loan, name='create_loan'),
    path('create_user/', create_user, name='create_user'),
    path('search_books/', search_books, name='search_books'),
    path('create_category/', create_category, name='create_category'),
    path('see_posts/', see_posts, name='see_posts'),
    path('edit_post/<int:post_id>', edit_post, name='edit_post'),
    # user side
    path('', home_page, name='homepage'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search_book/', search_book, name='search_book'),

]
