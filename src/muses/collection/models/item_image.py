from django.db import models
from django.utils.translation import ugettext_lazy as _

from six import python_2_unicode_compatible

__all__ = ('ItemImage',)


@python_2_unicode_compatible
class ItemImage(models.Model):
    """Item image."""

    item = models.ForeignKey('muses_collection.Item')
    image = models.ForeignKey('muses_collection.Image')

    class Meta(object):
        """Meta options."""

        verbose_name = _("Item image")
        verbose_name_plural = _("Item image")

    def __str__(self):
        return self.image_id
