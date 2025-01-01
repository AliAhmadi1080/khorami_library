from django import forms
from .models import Loan, Post, Category


class LoanForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields = '__all__'


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class BookSearchForm(forms.Form):
    name = forms.CharField(label='اسم کتاب', max_length=255, required=False)
    code = forms.CharField(label='کد کتاب', max_length=255, required=False)
    user = forms.CharField(label='نام متقاضی', max_length=255, required=False)
    is_return = forms.BooleanField(
        label='برگشتی', required=False, disabled=False)
