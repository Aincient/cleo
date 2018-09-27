from __future__ import absolute_import, unicode_literals

import logging
import os

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


from ...helpers import remove_image_from_drive
from ..helpers import make_images_active_and_download_files
from ..models.image import Image


__all__ = ('ImageAdmin',)

LOGGER = logging.getLogger(__name__)
REQUESTS_LOG = logging.getLogger("requests.packages.urllib3")
REQUESTS_LOG.setLevel(logging.DEBUG)
REQUESTS_LOG.propagate = True


def make_active_and_download_files(modeladmin, request, queryset):
    """Make selected images active and download them at once.

    - Make selected images active.
    - Downloads selected image files from the remote server.
    """
    counter = make_images_active_and_download_files(
        queryset=queryset,
        request=request
    )

    # Add info message
    messages.info(
        request,
        _("{} images downloaded/updated.").format(counter)
    )


make_active_and_download_files.short_description = _(
    'Make active and download files'
)


def make_inactive_and_delete_local_files(modeladmin, request, queryset):
    """Make selected images inactive.

    - Make selected images inactive.
    - Remove local image files.
    """
    images = queryset \
        .filter() \
        .exclude(image='') \
        .values_list('image', flat=True)

    for image in list(images):
        remove_image_from_drive(
            os.path.join(settings.MEDIA_ROOT, image)
        )

    queryset.update(active=False)


make_inactive_and_delete_local_files.short_description = _(
    'Make inactive and delete local files'
)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Image admin."""

    list_display = (
        'id',
        'api_url',
        'admin_web_image_url',
        'active',
        'created',
    )
    list_filter = (
        'active',
        'item__importer_uid'
    )
    search_fields = (
        'item__title_orig',
        'api_url',
    )

    actions = [
        make_active_and_download_files,
        make_inactive_and_delete_local_files,
    ]

    class Media(object):
        """Custom media."""

        js = ('collection/collection_admin.js',)

    def admin_web_image_url(self, obj):
        """

        :return:
        """
        if obj.active and obj.image and obj.image.url:
            _image_url = obj.image.url
        else:
            _image_url = obj.api_url

        return format_html(
            '''
            <a href="{}" target="_blank">
                <img src="{}" style="width: 250px; height: auto;"/>
            </a>
            ''',
            _image_url,
            _image_url
        )

    admin_web_image_url.short_description = _("Web image URL preview")
