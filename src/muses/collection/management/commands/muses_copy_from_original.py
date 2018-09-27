from __future__ import absolute_import, unicode_literals

import logging

from django.db.models import F, Q
from django.core.management.base import BaseCommand, CommandError

from muses.collection.constants import ALLOWED_COPY_FIELDS, DEFAULT_COPY_FIELDS
from muses.collection.helpers import translate_collection_items
from muses.collection.models import Item

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Copy from original."""

    help = "Translate."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--target-language',
                            type=str,
                            dest='target_language',
                            help="Target language.")
        parser.add_argument('--update-existing',
                            action='store_true',
                            dest='update_existing',
                            default=False,
                            help="Update existing translations.")
        parser.add_argument('--copy-fields',
                            type=str,
                            dest='copy_fields',
                            help="Fields to copy.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        update_existing = bool(options['update_existing'])
        target_language = str(options['target_language'])

        copy_fields = []
        if options['copy_fields']:
            copy_fields = [
                __val.strip()
                for __val
                in str(options['copy_fields']).split(',')
                if __val
            ]

            # Sanity checks
            diff = list(set(copy_fields) - set(ALLOWED_COPY_FIELDS))
            if diff:
                raise CommandError(
                    "The following fields can't be translated: {}".format(
                        ', '.join(diff)
                    )
                )

        if not copy_fields:
            copy_fields = DEFAULT_COPY_FIELDS

        update_kwargs = {
            '{}_{}'.format(__f, target_language): F('{}_orig'.format(__f))
            for __f in copy_fields
        }

        # update_kwargs = {
        #     'title_{}'.format(target_language): F('title_orig'),
        #     'description_{}'.format(target_language): F('description_orig'),
        #     'city_{}'.format(target_language): F('city_orig'),
        #     'country_{}'.format(target_language): F('country_orig'),
        #     'period_{}'.format(target_language): F('period_orig'),
        #     'object_type_{}'.format(target_language): F('object_type_orig'),
        #     'material_{}'.format(target_language): F('material_orig'),
        #     'keywords_{}'.format(target_language): F('keywords_orig'),
        #     'reign_{}'.format(target_language): F('reign_orig'),
        #     'classification_{}'.format(target_language):
        #         F('classification_orig'),
        # }

        filters = []
        if not update_existing:
            for field in ['title']:
                filters.append(
                    Q(**{"{}_{}__isnull".format(field, target_language): True})
                    | Q(**{"{}_{}__exact".format(field, target_language): ''})
                )

        # items = Item \
        #     .objects\
        #     .exclude(language_code_orig=target_language) \
        #     .update(**update_kwargs)

        items = Item \
            .objects \
            .filter(language_code_orig=target_language) \
            .filter(*filters) \
            .update(**update_kwargs)

        print(items)
