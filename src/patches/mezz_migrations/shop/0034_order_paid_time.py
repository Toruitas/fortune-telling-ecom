# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-08-24 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_auto_20170818_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_time',
            field=models.DateTimeField(null=True, verbose_name='Order paid time'),
        ),
    ]
