# Generated by Django 2.0.7 on 2018-08-02 07:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0031_auto_20180802_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=812688, null=True),
        ),
    ]
