# Generated by Django 2.0.7 on 2018-08-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_auto_20180802_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=833294, null=True),
        ),
        migrations.AlterField(
            model_name='productcode',
            name='product_code',
            field=models.BigIntegerField(unique=True),
        ),
    ]
