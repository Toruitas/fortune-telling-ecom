# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160827_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='frontpage',
            field=models.BooleanField(default=False, verbose_name='Display on Front Page'),
        ),
    ]
