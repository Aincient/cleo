"""
Run importer(s).
"""

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from ...importer import do_import

__all__ = (
    'Command',
)


class Command(BaseCommand):
    """Run importers."""

    help = "Run importers."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--importer',
                            dest='importer_uid',
                            action='store',
                            type=str,
                            help="Importer UID.")
        parser.add_argument('--limit',
                            action='store',
                            dest='limit',
                            type=int,
                            default=16000,
                            help="Number of records to import.")

        parsed, unknown = parser.parse_known_args()
        for arg in unknown:
            if arg.startswith(("-", "--")):
                # you can pass any arguments to add_argument
                parser.add_argument(arg,
                                    type=str)

    def handle(self, *args, **options):
        limit = options['limit']
        importer_uid = options['importer_uid']

        do_import(importer_uid, options)
