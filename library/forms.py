from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields = '__all__'

class BookSearchForm(forms.Form):
    name = forms.CharField(label='اسم کتاب', max_length=255, required=False)
    code = forms.CharField(label='کد کتاب', max_length=255, required=False)
    user = forms.CharField(label='نام متقاضی', max_length=255, required=False)
    is_return = forms.BooleanField(label='برگشتی', required=False, disabled=False)
