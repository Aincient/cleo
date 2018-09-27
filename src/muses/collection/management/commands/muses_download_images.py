from __future__ import absolute_import, unicode_literals

import importlib
import logging

from django.db.models import Q
from django.core.management.base import BaseCommand

from muses.collection.helpers import make_images_active_and_download_files
from muses.collection.models import Image as ItemImage

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Download images."""

    help = "Make images active and download files."

    requires_system_checks = False

    def add_arguments(self, parser):
        # parser.add_argument('--cache-results',
        #                     action='store_true',
        #                     dest='cache_results',
        #                     default=True,
        #                     help="Store results in cache.")
        parser.add_argument('--importer',
                            dest='importer_uid',
                            action='store',
                            type=str,
                            help="Importer UID.")

        parser.add_argument('--obtain-image-func',
                            dest='obtain_image_func',
                            action='store',
                            type=str,
                            help="Obtain image function.")

        parser.add_argument('--re-download-existing',
                            action='store_true',
                            dest='re_download_existing',
                            default=False,
                            help="Re-download existing active images.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        importer_uid = options['importer_uid']
        obtain_image_func = options['obtain_image_func']
        kwargs = {}
        if obtain_image_func:
            _module_name, _func_name = obtain_image_func.rsplit('.', 1)
            _module = importlib.import_module(_module_name)
            kwargs = {
                'obtain_image_func': getattr(_module, _func_name)
            }
        re_download_existing = bool(options['re_download_existing'])

        if re_download_existing is True:
            queryset = ItemImage.objects.exclude(
                Q(api_url__isnull=True) | Q(api_url__exact='')
            )
        else:
            queryset = ItemImage.objects.exclude(
                Q(api_url__isnull=True) | Q(api_url__exact='')
            ).filter(
                Q(image__isnull=True) | Q(image__exact=''),
            )

        if importer_uid:
            queryset = queryset.filter(item__importer_uid=importer_uid)

        counter = make_images_active_and_download_files(
            queryset=queryset,
            **kwargs
        )
        LOGGER.info("{} images downloaded/updated".format(counter))
