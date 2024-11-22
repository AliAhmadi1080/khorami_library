from django.urls import path
from .views import import_excle_file, dashbord, search

urlpatterns = [
    path('import_file', import_excle_file, name='import_excle_file'),
    path('dashbord', dashbord, name='dashbord'),
    path('', search, name='search'),

]
