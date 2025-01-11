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
    is_return = models.BooleanField(default=False)
    have_request = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} کتاب {self.book} را در \
            تاریخ {self.loan_date} قرض گرفته است."


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = jmodels.jDateField(auto_now_add=True)
    last_modified = jmodels.jDateField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name="posts")


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
        default=PROCESSING,  # مقدار پیش‌فرض
    )
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    request_date = jmodels.jDateField('تاریخ درخواست', auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} کتاب {self.book} را در \
            تاریخ {self.request_date} درخواست داده است."
