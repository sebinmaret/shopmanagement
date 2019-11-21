# Generated by Django 2.2.6 on 2019-11-08 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0006_auto_20191108_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(max_length=30, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='products',
            name='company',
            field=models.CharField(max_length=30, null=True, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.FloatField(null=True, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(null=True, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='products',
            name='typE',
            field=models.CharField(max_length=20, null=True, verbose_name='Type'),
        ),
    ]
