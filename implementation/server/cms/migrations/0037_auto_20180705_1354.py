# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-05 18:54
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0036_remove_homepage_hero_cta_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='hero_cta_link',
            field=models.CharField(blank=True, help_text='Hero Link', max_length=255, verbose_name='Hero Link'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sub_hero_block',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_text',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
