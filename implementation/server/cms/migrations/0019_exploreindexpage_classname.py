# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-02 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0018_auto_20180702_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='exploreindexpage',
            name='classname',
            field=models.CharField(blank=True, help_text='classname', max_length=255),
        ),
    ]