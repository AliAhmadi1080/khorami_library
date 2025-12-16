import re
from django.db import models
from account.models import CustomUser
from django_jalali.db import models as jmodels

def remove_all_numbers(text: str) -> str:
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[۰-۹]+', '', text)
    return text



class Book(models.Model):
    name = models.CharField('اسم', max_length=255, null=True)
    code = models.CharField('کد', max_length=255, null=True)
    row_number = models.PositiveBigIntegerField('ردیف', null=True)

    title = models.CharField('نام', max_length=255, null=True)
    author = models.CharField('نویسنده', max_length=255, null=True)
    publisher = models.CharField('ناشر', max_length=255, null=True)
    year = models.PositiveIntegerField('سال نشر', null=True)
    notes = models.CharField('متفرقه', max_length=255, null=True)
    

    embedding = models.JSONField(null=True, blank=True)
    
    complited = models.BooleanField('کامل شده؟', default=False)
    has_embedding = models.BooleanField('دارای امبدینگ؟', default=False)
    def generate_search_text(self) -> str:
        text_parts = []
        
        if self.complited:
            text_parts.append(f"کتاب {self.title}")
            text_parts.append(f"نویسنده {self.author}")
            text_parts.append(f"ناشر {self.publisher}")
            text_parts.append(f"سال نشر {self.year}")
            text_parts.append(f"کد کتاب {remove_all_numbers(self.code)}")

        if self.notes :
            text_parts.append(self.notes)
        
        return " ".join(text_parts)

    def __str__(self) -> str:
        return f'{self.name}--{self.code}'


class Loan(models.Model):
    book = models.ForeignKey(Book, verbose_name='کتاب',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, verbose_name='متقاضی', on_delete=models.CASCADE)
    loan_date = jmodels.jDateField('تاریخ تحویل', auto_now_add=True)
    return_date = jmodels.jDateField('تاریخ بازگشت')
    is_return = models.BooleanField(default=False)
    have_request = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} کتاب {self.book} را در \
            تاریخ {self.loan_date} قرض گرفته است."



class Request(models.Model):
    PROCESSING = 'processing'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'

    STATUS_CHOICES = [
        (PROCESSING, 'در حال پردازش'),
        (REJECTED, 'رد درخواست'),
        (ACCEPTED, 'پذیرش درخواست'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PROCESSING,  
    )
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    request_date = jmodels.jDateField('تاریخ درخواست', auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} کتاب {self.book} را در \
            تاریخ {self.request_date} درخواست داده است."

