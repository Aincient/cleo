# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-05 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailtrans', '0007_auto_20180327_1127'),
        ('cms', '0031_auto_20180705_0747'),
    ]
    migrations.RunSQL(
            """
            BEGIN;

            -- Remove constraints so we can edit our table
            ALTER TABLE cms_formpage DROP CONSTRAINT cms_formpage_pkey CASCADE;

            -- Add ``translatablepage_ptr_id`` field and copy the ``page_ptr_id`` content
            ALTER TABLE cms_formpage ADD COLUMN translatablepage_ptr_id INTEGER UNIQUE;
            UPDATE cms_formpage SET translatablepage_ptr_id=page_ptr_id;

            -- Insert the required values in ``wagtailtrans`` table
            INSERT INTO wagtailtrans_language (code, is_default, position, live) SELECT 'en', 't', 0, 't' WHERE NOT EXISTS (SELECT code FROM wagtailtrans_language WHERE code='en');
            INSERT INTO wagtailtrans_translatablepage (translatable_page_ptr_id, canonical_page_id, language_id) SELECT translatablepage_ptr_id, NULL, 1 FROM cms_formpage;

            -- Add required indexes and constraints
            ALTER TABLE cms_formpage ADD CONSTRAINT cms_formpage_translatablepage_ptr_id_e5b77cf7_fk_wagtailtrans_translatable_page_id FOREIGN KEY (translatablepage_ptr_id) REFERENCES wagtailtrans_translatablepage (translatable_page_ptr_id) DEFERRABLE INITIALLY DEFERRED;
            ALTER TABLE cms_formpage ALTER COLUMN translatablepage_ptr_id SET NOT NULL;
            ALTER TABLE cms_formpage ADD PRIMARY KEY (translatablepage_ptr_id);

            COMMIT;
            """,
            state_operations=[
                migrations.RemoveField(
                    model_name='people',
                    name='image',
                ),
                migrations.RemoveField(
                    model_name='homepage',
                    name='advert',
                ),
                migrations.AddField(
                    model_name='formpage',
                    name='translatablepage_ptr',
                    field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailtrans.TranslatablePage'),
                    preserve_default=False,
                ),
                migrations.AlterField(
                    model_name='formpage',
                    name='page_ptr',
                    field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='wagtailcore.Page'),
                ),
                migrations.DeleteModel(
                    name='People',
                ),
            ]
        ),

