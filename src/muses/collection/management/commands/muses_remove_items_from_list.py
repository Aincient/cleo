from __future__ import absolute_import, unicode_literals

import logging

from django.core.management.base import BaseCommand

from muses.collection.inventory_number_list import REMOVE_LIST
from muses.collection.models import Item
from muses.collection.helpers import remove_item_list


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Fix wrong translations."""

    help = "Remove items from a list of inventory numbers."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--importer',
                            dest='importer_uid',
                            action='store',
                            type=str,
                            help="Importer UID.")
        parser.add_argument('--dry-run',
                            action='store_true',
                            dest='dry_run',
                            default=False,
                            help="Dry-run (don't delete, only show which "
                                 "ones are going to be removed).")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        importer_uid = options['importer_uid']
        dry_run = options['dry_run']
        q = Item.objects.all()
        if importer_uid:
            q = q.filter(importer_uid=importer_uid)
        l = REMOVE_LIST

        remove_item_list(l, dry_run, q)
