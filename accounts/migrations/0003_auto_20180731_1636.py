# Generated by Django 2.0.7 on 2018-07-31 16:36

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180731_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='code',
            field=models.CharField(max_length=4, unique=True, validators=[accounts.models.validate_code_length]),
        ),
    ]
