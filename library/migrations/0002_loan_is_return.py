# Generated by Django 5.1.3 on 2024-12-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='is_return',
            field=models.BooleanField(default=False),
        ),
    ]
