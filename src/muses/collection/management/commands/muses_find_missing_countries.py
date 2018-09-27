from __future__ import absolute_import, unicode_literals

import logging

from django.db.models import F, Q
from django.core.management.base import BaseCommand, CommandError

from muses.collection.models import Item
from muses.collection.helpers import find_missing_countries

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Find countries for items that have a city but not a country."""

    help = "Find missing countries."

    requires_system_checks = False

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """

        items = Item \
            .objects \
            .exclude(Q(city_en__isnull=True) | Q(city_en__exact=''),) \
            .filter(Q(country_en__isnull=True) | Q(country_en__exact=''),)

        find_missing_countries(items)

