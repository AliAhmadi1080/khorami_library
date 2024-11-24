from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import render
from .models import Book
import pandas as pd
import pdfplumber
import threading


def handle_uploaded_file(f):
    with open("files/name.pdf", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    pdf_path = 'files/name.pdf'  # Replace with your PDF file path
    rows_list = []
    Book.objects.all().delete()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    numbetsdone = 0
                    text = ''
                    for char in row[1][::-1]:
                        if not char.isdigit():
                            text += char
                            numbetsdone = 0
                        else:
                            if numbetsdone == 0:
                                text += char
                                numbetsdone += 1
                            else:
                                text = text[:-1 * numbetsdone] + \
                                    char + text[-1 * numbetsdone:]
                                numbetsdone += 1
                    row[1] = text
                    rows_list.append(row)
    df = pd.DataFrame(rows_list[1:], columns=rows_list[0])
    df.columns = ['code', "name", 'row_number']
    for index, row in df.iterrows():
        try:
            book = Book.objects.create(
                name=row['name'], code=row['code'],
                row_number=int(row['row_number']))
        except:
            pass


@login_required
def import_excle_file(request: HttpRequest):
    context = {}
    if request.method == 'POST':
        file = request.FILES["inputfile"]
        t1 = threading.Thread(target=handle_uploaded_file, args=(file,))
        t1.start()
        context['succses'] = True
    return render(request, 'library\inputfile.html', context)


@login_required
def dashbord(request: HttpRequest):
    context = {}
    return render(request, 'library\dashbord.html', context)


def search(request: HttpRequest):
    input = request.GET.get('input', None)
    books = Book.objects.filter(name__contains=input if input else '')
    if input is None:
        books = books[:20]
    context = {'books': books, 'count': Book.objects.all().count()
               if not input else books.count()}
    return render(request, 'library\search.html', context)
