# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 22:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20170419_2234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Company',
            new_name='Companies',
        ),
        migrations.AlterModelTable(
            name='companies',
            table='Companies',
        ),
    ]
