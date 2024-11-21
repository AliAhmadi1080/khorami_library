from django.shortcuts import render
from django.http.request import HttpRequest


def import_excle_file(request:HttpRequest):
    context = {}
    if request.method == 'POST':
        print(request.FILES) #TODO: compolit it
        context['succses'] = True
    return render(request, 'library\inputfile.html', context)


def dashbord(request):
    context = {}
    return render(request, 'library\dashbord.html', context)
