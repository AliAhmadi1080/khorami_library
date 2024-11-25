from django.urls import path
from django.contrib.auth import views
from .views import import_excle_file, dashbord, search, createuser

urlpatterns = [
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path('import_file/', import_excle_file, name='import_excle_file'),
    path('dashbord/', dashbord, name='dashbord'),
    path('createuser/', createuser, name='createuser'),
    path('', search, name='search'),

]
