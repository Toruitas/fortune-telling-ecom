# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
