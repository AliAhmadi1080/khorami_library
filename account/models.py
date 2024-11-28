from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, joined_number, fullname, classname, password=None, **extra_fields):
        if not joined_number:
            raise ValueError('The Joined Number field must be set')
        user = self.model(joined_number=joined_number, fullname=fullname, classname=classname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, joined_number, fullname, classname, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(joined_number, fullname, classname, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
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
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    fullname = models.CharField('نام و نام خانوادگی', max_length=255)
    classname = models.CharField('کلاس', max_length=20, choices=CLASSNAME_CHOICES)
    joined_number = models.PositiveBigIntegerField('شماره عضویت',unique=True)
    username = models.CharField(unique=True,max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', 'classname','joined_number']

    def __str__(self):
        return self.fullname
