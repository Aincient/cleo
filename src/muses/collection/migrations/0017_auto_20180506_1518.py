# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-06 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muses_collection', '0016_auto_20180506_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='period_start_nl',
            new_name='object_date_begin_nl',
        ),
    ]
