"""
Run importer update.
"""

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from ...importer import do_update

__all__ = (
    'Command',
)


class Command(BaseCommand):
    """Run importer data update."""

    help = "Run importer data update."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--importer',
                            dest='importer_uid',
                            action='store',
                            type=str,
                            help="Importer UID.")
        parser.add_argument('--fields',
                            action='store',
                            dest='fields',
                            type=str,
                            help="(database) fields to update.")

        parsed, unknown = parser.parse_known_args()
        for arg in unknown:
            if arg.startswith(("-", "--")):
                # you can pass any arguments to add_argument
                parser.add_argument(
                    arg,
                    type=str
                )

    def handle(self, *args, **options):
        importer_uid = options['importer_uid']
        _fields = options['fields']
        fields = [__f.strip() for __f in _fields.split(',') if __f]

        _counter = do_update(
            importer_uid=importer_uid,
            options=options,
            fields=fields
        )

        print(_counter)
