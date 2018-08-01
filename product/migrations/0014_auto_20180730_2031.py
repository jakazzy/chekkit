# Generated by Django 2.0.7 on 2018-07-30 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_auto_20180730_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'verbose_name': 'Batch Number', 'verbose_name_plural': 'Batch Numbers'},
        ),
        migrations.AddField(
            model_name='batch',
            name='product_line',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.ProductLine'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='batch',
            name='batch_number',
            field=models.IntegerField(blank=True, default=859070, null=True, unique=True),
        ),
    ]
