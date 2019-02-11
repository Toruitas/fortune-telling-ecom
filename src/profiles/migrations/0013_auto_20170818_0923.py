# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-08-18 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20170703_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='direction_1',
            field=models.CharField(blank=True, choices=[('n', 'North'), ('nw', 'Northwest'), ('w', 'West'), ('sw', 'Southwest'), ('s', 'South'), ('se', 'Southeast'), ('e', 'East'), ('ne', 'Northeast')], max_length=100, null=True, verbose_name='Direction of Primary Location'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='direction_2',
            field=models.CharField(blank=True, choices=[('n', 'North'), ('nw', 'Northwest'), ('w', 'West'), ('sw', 'Southwest'), ('s', 'South'), ('se', 'Southeast'), ('e', 'East'), ('ne', 'Northeast')], max_length=100, null=True, verbose_name='Direction of Secondary Location'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='direction_3',
            field=models.CharField(blank=True, choices=[('n', 'North'), ('nw', 'Northwest'), ('w', 'West'), ('sw', 'Southwest'), ('s', 'South'), ('se', 'Southeast'), ('e', 'East'), ('ne', 'Northeast')], max_length=100, null=True, verbose_name='Direction of Third Location'),
        ),
    ]
