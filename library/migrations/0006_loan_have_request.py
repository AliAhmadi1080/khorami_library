# Generated by Django 5.1.3 on 2025-01-11 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_category_name_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='have_request',
            field=models.BooleanField(default=False),
        ),
    ]
