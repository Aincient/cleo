from __future__ import absolute_import, unicode_literals

import logging

from django.core.management.base import BaseCommand, CommandError

from muses.collection.helpers import find_period_collection_items

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Normalize period names."""

    help = "Normalize period names."

    requires_system_checks = False

    def add_arguments(self, parser):
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
        update_existing = bool(options['update_existing'])

        find_period_collection_items(
            update_existing=update_existing
        )
