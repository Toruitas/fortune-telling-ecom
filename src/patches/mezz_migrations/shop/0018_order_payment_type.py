# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-23 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20170323_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='payment_type'),
        ),
    ]
