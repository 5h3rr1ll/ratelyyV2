# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 17:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_auto_20170524_1904'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brands',
            new_name='Brand',
        ),
        migrations.AlterModelTable(
            name='brand',
            table='Brand',
        ),
    ]
