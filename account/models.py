from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomeUser(AbstractUser):
    CLASSNAME_CHOICES = (
        ("7.1", "7.1"),
        ("7.2", "7.2"),
        ("7.3", "7.3"),
        ("8.1", "8.1"),
        ("8.2", "8.2"),
        ("8.3", "8.3"),
        ("9.1", "9.1"),
        ("9.2", "9.2"),
        ("9.3", "9.3"),
    )
    fullname = models.CharField('نام و نام خانوادگی', max_length=255)
    classname = models.CharField(
        'کلاس', max_length=20, choices=CLASSNAME_CHOICES)
    joined_number = models.PositiveBigIntegerField('شماره عضویت', null=True)
    
