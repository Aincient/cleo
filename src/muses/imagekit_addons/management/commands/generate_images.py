from django.core.management.base import BaseCommand, CommandError

from imagekit.registry import generator_registry, cachefile_registry
from imagekit.exceptions import MissingSource


class Command(BaseCommand):
    help = (
        "Generate files for the specified image generators (or all of them "
        "if none was provided). Simple, comma-separated list."
    )

    def add_arguments(self, parser):
        parser.add_argument('--generator-ids',
                            type=str,
                            dest='generator_ids',
                            help="Generator IDs.")

    def handle(self, *args, **options):
        generators = generator_registry.get_ids()

        generator_ids = [
            __val.strip()
            for __val
            in str(options['generator_ids']).split(',')
            if __val
        ]

        # Sanity checks
        diff = list(set(generator_ids) - set(list(generators)))
        if diff:
            raise CommandError(
                "The following generator ids are not registered {}".format(
                    ', '.join(diff)
                )
            )
        for generator_id in generators:
            self.stdout.write('Validating generator: %s\n' % generator_id)
            for image_file in cachefile_registry.get(generator_id):
                if image_file.name:
                    self.stdout.write('  %s\n' % image_file.name)
                    try:
                        image_file.generate()
                    except MissingSource as err:
                        self.stdout.write('\t No source associated with\n')
                    except Exception as err:
                        self.stdout.write('\tFailed %s\n' % (err))
