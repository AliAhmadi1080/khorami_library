from django.db import models


class Book(models.Model):
    name = models.CharField('اسم', max_length=255, null=True, blank=True)
    code = models.CharField('کد', max_length=255, null=True, blank=True)
    row_number = models.PositiveBigIntegerField('ردیف', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}--{self.code}'
