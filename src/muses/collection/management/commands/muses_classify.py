from __future__ import absolute_import, unicode_literals

import json
import logging

from django.conf import settings
from django.db.models import Q, Count
from django.core.management.base import BaseCommand

from muses.collection.models import Item
from muses.naive_classification.helpers_os import predict_image_path_dict

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Classify."""

    help = "Classify items with our AI."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--update-existing',
                            action='store_true',
                            dest='update_existing',
                            default=False,
                            help="Update existing classifications.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        update_existing = bool(options['update_existing'])

        filters = []
        if not update_existing:
            for field in ['classified_as']:
                filters.append(
                    Q(**{"{}__isnull".format(field): True})
                    | Q(**{"{}__exact".format(field): ''})
                )

        items = Item \
            .objects \
            .filter(*filters) \
            .prefetch_related('images') \
            .annotate(num_images=Count('images')) \
            .filter(num_images__gt=0)

        for item in items:
            paths = []
            for image in item.images.all():
                try:
                    paths.append(image.image.path)
                except Exception as err:
                    LOGGER.warning(err)

            conf = settings \
                .MUSES_CONFIG['classification']['naive_classification']
            model_path = conf['model_path']

            try:
                classification = predict_image_path_dict(
                    paths,
                    model_path=model_path
                )
            except Exception as err:
                LOGGER.warning(err)
                continue

            top_results = list(classification.items())[:5]
            if top_results:
                try:
                    item.classified_as = top_results
                    item.save()
                except Exception as err:
                    pass
