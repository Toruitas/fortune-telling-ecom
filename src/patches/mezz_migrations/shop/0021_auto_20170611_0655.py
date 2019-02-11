# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-06-11 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_product_frontbanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='frontbanner',
            field=models.BooleanField(default=False, verbose_name='Display on home banner slider'),
        ),
        migrations.AlterField(
            model_name='product',
            name='frontpage',
            field=models.BooleanField(default=False, verbose_name='Display on Front Page products'),
        ),
    ]
