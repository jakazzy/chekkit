# Generated by Django 2.0.7 on 2018-08-02 20:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0038_auto_20180802_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=598886, null=True),
        ),
    ]