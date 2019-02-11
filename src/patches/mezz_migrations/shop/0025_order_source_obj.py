# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-07-19 04:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20170718_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='source_obj',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='source_obj'),
        ),
    ]
