# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_brands_urlzumhersteller'),
    ]

    operations = [
        migrations.AddField(
            model_name='brands',
            name='altName',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
