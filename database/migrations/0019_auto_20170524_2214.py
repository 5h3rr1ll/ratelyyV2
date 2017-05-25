# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_auto_20170524_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='newBrandByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('fair', models.IntegerField()),
                ('eco', models.IntegerField()),
                ('url', models.CharField(max_length=50, null=True)),
                ('counter', models.CharField(default=0, max_length=1000)),
            ],
            options={
                'db_table': 'newBrandByUsers',
            },
        ),
        migrations.CreateModel(
            name='newCompanyByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('fair', models.IntegerField()),
                ('eco', models.IntegerField()),
                ('url', models.CharField(max_length=50, null=True)),
                ('counter', models.CharField(default=0, max_length=1000)),
            ],
            options={
                'db_table': 'newCompanyByUsers',
            },
        ),
        migrations.CreateModel(
            name='newProductByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('fair', models.IntegerField()),
                ('eco', models.IntegerField()),
                ('url', models.CharField(max_length=50, null=True)),
                ('counter', models.CharField(default=0, max_length=1000)),
            ],
            options={
                'db_table': 'newProductByUsers',
            },
        ),
        migrations.RenameModel(
            old_name='Companie',
            new_name='Company',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.AlterModelTable(
            name='company',
            table='Company',
        ),
        migrations.AlterModelTable(
            name='product',
            table='Product',
        ),
    ]
