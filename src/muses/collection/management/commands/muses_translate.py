from __future__ import absolute_import, unicode_literals

import logging

from django.core.management.base import BaseCommand, CommandError

from muses.collection.helpers import translate_collection_items
from muses.collection.constants import (
    ALLOWED_TRANSLATED_FIELDS,
    DEFAULT_TRANSLATED_FIELDS,
)

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Translate."""

    help = "Translate."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--target-language',
                            type=str,
                            dest='target_language',
                            help="Target language.")
        parser.add_argument('--translated-fields',
                            type=str,
                            dest='translated_fields',
                            help="Translated fields.")
        parser.add_argument('--use-cache',
                            action='store_true',
                            dest='use_cache',
                            default=False,
                            help="Use cache for storing and retrieving "
                                 "of the results.")
        parser.add_argument('--update-existing',
                            action='store_true',
                            dest='update_existing',
                            default=False,
                            help="Update existing translations.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        use_cache = bool(options['use_cache'])
        update_existing = bool(options['update_existing'])
        target_language = str(options['target_language'])

        translated_fields = []

        if options['translated_fields']:
            translated_fields = [
                __val.strip()
                for __val
                in str(options['translated_fields']).split(',')
                if __val
            ]

            # Sanity checks
            diff = list(
                set(translated_fields) - set(ALLOWED_TRANSLATED_FIELDS)
            )
            if diff:
                raise CommandError(
                    "The following fields can't be translated {}".format(
                        ', '.join(diff)
                    )
                )

        if not translated_fields:
            translated_fields = DEFAULT_TRANSLATED_FIELDS

        translate_collection_items(
            target_language=target_language,
            translated_fields=translated_fields,
            use_cache=use_cache,
            update_existing=update_existing
        )
