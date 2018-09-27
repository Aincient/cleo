from __future__ import absolute_import, unicode_literals

import logging
import re

from django.core.management.base import BaseCommand

from muses.cached_api_calls.models import TranslationFix
from muses.cached_api_calls.models.translation_fix import FIELD_CHOICES
from muses.collection.models import Item


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Fix wrong translations."""

    help = "Fix wrong translations."

    requires_system_checks = False

    def handle(self, *args, **options):
        """Handle.

        :param args:
        :param options:
        :return:
        """
        for translation in TranslationFix.objects.all():
            if translation.exact_match:
                lookup = '__iexact'
            else:
                lookup = '__icontains'
            if translation.field == 'all':
                fields = [
                    '{}_{}'.format(choice[0], translation.language)
                    for choice
                    in FIELD_CHOICES
                    if choice[0] != 'all'
                    ]
            else:
                fields = [translation.field_name()]

            for field in fields:
                field_lookup = '{}{}'.format(field, lookup)
                items = Item.objects.filter(**{field_lookup: translation.original}).only(field)
                for item in items:
                    setattr(
                        item,
                        field,
                        re.sub(r"\b" + re.escape(translation.original) + r"\b",
                               translation.replacement, getattr(item, field))
                    )
                    item.save()

        # Hardcoded the fix that items that have Misr listed as city should have Egypt as country
        # Because it is a prevalent issue, and it seems easiest to do it like this
        Item.objects.filter(
            city_orig__iexact='Misr'
        ).update(
            country_en='Egypt',
            country_nl='Egypte'
        )
