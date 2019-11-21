# Generated by Django 2.2.6 on 2019-11-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0012_auto_20191109_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('p_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Product ID')),
                ('p_type', models.CharField(max_length=20, verbose_name='Type')),
                ('company', models.CharField(max_length=30, verbose_name='Company')),
                ('category', models.CharField(max_length=30, verbose_name='Category')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('price', models.FloatField(verbose_name='Price')),
                ('total_price', models.IntegerField(verbose_name='Total Price')),
            ],
        ),
    ]
