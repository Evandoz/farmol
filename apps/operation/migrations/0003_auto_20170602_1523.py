# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-02 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20170602_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userordertable',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='\u91d1\u989d'),
        ),
    ]