# Generated by Django 2.0.7 on 2018-08-02 20:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ussdapp', '0005_auto_20180802_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ussdrecord',
            name='session_id',
            field=models.CharField(max_length=140, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='ussdrecord',
            unique_together=set(),
        ),
    ]