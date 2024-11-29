from django.db import models
from account.models import CustomUser
from django_jalali.db import models as jmodels


class Book(models.Model):
    name = models.CharField('اسم', max_length=255, null=True, blank=True)
    code = models.CharField('کد', max_length=255, null=True, blank=True)
    row_number = models.PositiveBigIntegerField('ردیف', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}--{self.code}'


class Loan(models.Model):
    book = models.ForeignKey(Book, verbose_name='کتاب',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, verbose_name='متقاضی', on_delete=models.CASCADE)
    loan_date = jmodels.jDateField('تاریخ تحویل', auto_now_add=True)
    return_date = jmodels.jDateField('تاریخ بازگشت')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} کتاب {self.book} را در \
            تاریخ {self.loan_date} قرض گرفته است."
