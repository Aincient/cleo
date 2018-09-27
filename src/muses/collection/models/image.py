from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeCanvas

from six import python_2_unicode_compatible

__all__ = ('Image',)


@python_2_unicode_compatible
class Image(models.Model):
    """Image model."""

    # *******************************************************************
    # ******************** Language independent data ********************
    # *******************************************************************
    api_url = models.TextField(
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Image API URL"),
    )
    primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary image")
    )
    image = models.FileField(
        null=True,
        blank=True,
        upload_to='collection_images',
        verbose_name=_("Image"),
    )
    image_large = ImageSpecField(
        source='image',
        processors=[
            ResizeToFit(960, 960, upscale=False),
        ],
        format='JPEG',
        options={'quality': 85, 'suffix': '_large'}
    )
    image_sized = ImageSpecField(
        source='image_large',
        processors=[
            ResizeToFit(108, 108, upscale=False),
            ResizeCanvas(128, 128),
        ],
        format='JPEG',
        options={'quality': 90, 'suffix': '_sized'}
    )
    image_ml = ImageSpecField(
        source='image_large',
        processors=[
            ResizeToFit(108, 108, upscale=False),
            ResizeCanvas(128, 128),
        ],
        format='PNG',
        options={'quality': 90, 'suffix': '_ml'}
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_("Active"),
    )
    trimmed = models.BooleanField(
        default=False,
        verbose_name=_("Trimmed"),
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name=_("Date imported"),
    )
    updated = models.DateField(
        auto_now=True,
        verbose_name=_("Date updated"),
    )

    # *******************************************************************
    # ******************** Data translated into English *****************
    # *******************************************************************
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Title of the object")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Description of the object")
    )

    # *******************************************************************
    # ******************** Original data as imported ********************
    # *******************************************************************
    title_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original title"),
        help_text=_("Title of the object")
    )
    description_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original description"),
        help_text=_("Description of the object")
    )

    class Meta(object):
        """Meta options."""

    def __str__(self):
        return self.api_url
