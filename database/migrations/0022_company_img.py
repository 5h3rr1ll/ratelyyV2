# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20170528_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='img',
            field=models.CharField(max_length=50, null=True),
        ),
    ]