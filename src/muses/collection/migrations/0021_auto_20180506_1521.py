# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-06 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muses_collection', '0020_auto_20180506_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='period_end_orig',
            new_name='object_date_end_orig',
        ),
    ]