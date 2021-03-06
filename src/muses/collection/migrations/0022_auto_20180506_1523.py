# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-06 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muses_collection', '0021_auto_20180506_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='period_en',
            field=models.TextField(blank=True, null=True, verbose_name='Period (EN)'),
        ),
        migrations.AddField(
            model_name='item',
            name='period_nl',
            field=models.TextField(blank=True, null=True, verbose_name='Period (NL)'),
        ),
        migrations.AddField(
            model_name='item',
            name='period_orig',
            field=models.TextField(blank=True, null=True, verbose_name='Original period'),
        ),
    ]
