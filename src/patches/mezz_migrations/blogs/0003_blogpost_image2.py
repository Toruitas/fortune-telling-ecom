# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-12 10:18
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image2',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='Image 2'),
        ),
    ]
