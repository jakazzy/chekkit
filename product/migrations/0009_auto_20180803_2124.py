# Generated by Django 2.0.7 on 2018-08-03 21:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0008_auto_20180803_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=992334, null=True),
        ),
    ]