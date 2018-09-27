from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from six import python_2_unicode_compatible

__all__ = (
    'Period',
)


@python_2_unicode_compatible
class Period(MPTTModel):
    """Period."""

    name_en = models.TextField(
        verbose_name=_("English name"),
        unique=True
    )
    name_nl = models.TextField(
        verbose_name=_("Dutch name"),
        blank=True,
        null=True,
        unique=False,
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )
    date_begin_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Date begin (EN)"),
    )
    date_end_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Date end (EN)"),
    )

    class MPTTMeta(object):
        order_insertion_by = ['name_en']

    def date_range(self):
        """Get a string of the date range of a period, if available

        :return:
        :rtype: str
        """
        if self.date_begin_en and self.date_end_en:
            return "{} until {}".format(self.date_begin_en, self.date_end_en)

    def __str__(self):
        return self.name_en

