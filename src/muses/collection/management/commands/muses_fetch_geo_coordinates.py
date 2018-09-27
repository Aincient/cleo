from __future__ import absolute_import, unicode_literals

import logging

from django.core.management.base import BaseCommand, CommandError

from muses.collection.helpers import fetch_geo_coordinates_collection_items

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Translate."""

    help = "Translate."

    requires_system_checks = False

    def add_arguments(self, parser):
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

        fetch_geo_coordinates_collection_items(
            use_cache=use_cache,
            update_existing=update_existing
        )
