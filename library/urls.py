from django.urls import path
from django.contrib.auth import views
from .views import (import_excle_file, dashbord, undo_loan,
                    search, create_user, create_loan)

urlpatterns = [
    path("account/login/", views.LoginView.as_view(), name="login"),
    path('import_file/', import_excle_file, name='import_excle_file'),
    path('dashbord/', dashbord, name='dashbord'),
    path('undo_return/<int:loan_id>', undo_loan, name='undo_return'),
    path('create_loan/', create_loan, name='create_loan'),
    path('create_user/', create_user, name='create_user'),
    path('', search, name='search'),

]
