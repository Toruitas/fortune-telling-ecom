# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-27 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogpost_frontpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='content2',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='content3',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='content4',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='content5',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='content6',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image4',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image5',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image6',
        ),
    ]
