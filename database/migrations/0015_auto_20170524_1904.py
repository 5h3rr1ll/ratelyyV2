# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 17:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_auto_20170524_1855'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Companies',
            new_name='Companie',
        ),
        migrations.AlterModelTable(
            name='companie',
            table='Companie',
        ),
    ]