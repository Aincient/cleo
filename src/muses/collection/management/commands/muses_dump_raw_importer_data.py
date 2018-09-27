from __future__ import absolute_import, unicode_literals

import tablib
import logging

from django.db.models import Q
from django.core.management.base import BaseCommand

from muses.importers.metmuseum_org.helpers import MetropolitanClient
from muses.importers.brooklynmuseum_org.helpers import BrooklynClient
from muses.importers.thewalters_org.helpers import TheWaltersClient
from muses.importers.rmo_nl.helpers import NationalMuseumOfAntiquitiesClient

LOGGER = logging.getLogger(__name__)


MAPPING = {
    'rmo_nl': NationalMuseumOfAntiquitiesClient,
    'brooklynmuseum_org': BrooklynClient,
    'metmuseum_org': MetropolitanClient,
    'thewalters_org': TheWaltersClient,
}


class Command(BaseCommand):
    """Dump raw importers data."""

    help = "Dump raw importers data."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--importer',
                            dest='importer_uid',
                            action='store',
                            type=str,
                            help="Importer UID.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        importer_uid = options['importer_uid']
        client_cls = MAPPING.ge(importer_uid)
        client = client_cls()
        client.configure_from_settings()
        data = client.load_objects_from_json_cache()
        first_row = data[0]
        titles = [key for key in (data.keys())]
        values = [value for value in data.values()]
        # TODO
