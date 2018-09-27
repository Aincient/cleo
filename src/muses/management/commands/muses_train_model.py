from __future__ import absolute_import, unicode_literals

import logging

import os
from django.conf import settings
from muses.naive_classification.helpers import setup_classifier
from django.core.management.base import BaseCommand

LOGGER = logging.getLogger(__name__)
IMAGE_PATH = os.path.join(
                settings.BASE_DIR,
                '..',
                '..',
                'src',
                'muses',
                'naive_classification',
                'plots'
            )


class Command(BaseCommand):
    """Train model."""

    help = "Train a classification model"

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--model-name',
                            type=str,
                            dest='model_name',
                            help="Name of the trained model.")
        parser.add_argument('--epochs',
                            type=int,
                            dest='epochs',
                            help="Number of epochs to train.")
        parser.add_argument('--plot-performance',
                            action='store_true',
                            default=False,
                            dest='plot_performance',
                            help="Set to true if performance should be plotted.")
        parser.add_argument('--fine-tuning',
                            action='store_true',
                            default=True,
                            dest='finetuning',
                            help="Set to true if you want to fine-tune the model.")

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        plotting = bool(options['plot_performance'])
        finetuning = bool(options['finetuning'])
        name = str(options['model_name'])
        epochs = int(options['epochs'])
        image_location = '{}/{}'.format(IMAGE_PATH, name)

        # If you use fine-tuning, spend 2/3 of the epochs on transer learning
        # and 1/3 on fine-tuning
        if finetuning:
            transfer_epochs = int(epochs/1.5)
            fine_epochs = int(epochs/3)
        else:
            transfer_epochs = options['epochs']

        c = setup_classifier((128, 128))
        c.unfreeze_layers(0)
        c.train_model(transfer_epochs, weighted=True, save=True, model_name=name)
        c.plot_performance(image_location)
        if finetuning:
            c.unfreeze_layers(4)
            c.set_optimizer(lr=0.00005, decay=0)
            c.train_model(fine_epochs, weighted=True, save=True, model_name='{}_finetuned'.format(name))
            c.plot_performance('{}_finetuned'.format(image_location))
