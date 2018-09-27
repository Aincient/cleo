"""
Export classification data.
"""

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from ...exporter import do_export

__all__ = (
    'Command',
)


class Command(BaseCommand):
    """Run importers."""

    help = "Export classification data."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--exporter',
                            dest='exporter_uid',
                            action='store',
                            type=str,
                            help="Exporter UID.")
        parser.add_argument('--limit',
                            action='store',
                            dest='limit',
                            type=int,
                            default=16000,
                            help="Number of records to import.")

    def handle(self, *args, **options):
        limit = options['limit']
        exporter_uid = options['exporter_uid']

        do_export(exporter_uid)
