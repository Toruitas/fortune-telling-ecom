# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-07-24 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170611_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='blogpage',
            field=models.BooleanField(default=False, verbose_name='Show on Blog List'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='frontpage',
            field=models.BooleanField(default=False, verbose_name='Show on Home'),
        ),
    ]
