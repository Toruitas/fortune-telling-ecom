# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-05-18 11:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogpost_frontbanner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='frontbanner',
        ),
    ]
