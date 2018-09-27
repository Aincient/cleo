from __future__ import absolute_import, unicode_literals

import logging

from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ...importer import do_import
from ..models.item import Item


__all__ = ('ItemAdmin',)

LOGGER = logging.getLogger(__name__)
REQUESTS_LOG = logging.getLogger("requests.packages.urllib3")
REQUESTS_LOG.setLevel(logging.DEBUG)
REQUESTS_LOG.propagate = True


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Item admin."""

    list_display = (
        'id',
        'record_number',
        'inventory_number',
        # Title
        'title_orig',
        'title_en',
        'title_nl',
        # City, country orig
        'city_orig',
        'country_orig',
        # City, country eng
        'city_en',
        'country_en',
        # City, country nl
        'city_nl',
        'country_nl',
        # Object types orig, en, nl
        'object_type_orig',
        'object_type_en',
        'object_type_nl',
        'geo_location',
        'created',
        'updated'
    )
    list_filter = (
        'importer_uid',
        # 'city_orig',
        # 'country_orig',
        'object_type_orig',
    )
    search_fields = (
        'id',
        'title_en',
        'title_nl',
        'title_orig',
        'description_en',
        'description_orig',
        'record_number',
        'inventory_number',
    )
    readonly_fields = (
        'images',
        'created',
        'updated',
        'period_node_name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'importer_uid',
                'record_number',
                'inventory_number',
                'api_url',
                'web_url',
                'images',
                'geo_location',
                'created',
                'updated',
                'language_code_orig',
                'period_node_name'
            )
        }),
        ('Original', {
            'classes': ('normal',),
            'fields': (
                'title_orig',
                'description_orig',
                'department_orig',
                'dimensions_orig',
                'city_orig',
                'object_date_orig',
                'object_date_begin_orig',
                'object_date_end_orig',
                'period_orig',
                'dynasty_orig',
                'country_orig',
                'object_type_orig',
                'material_orig',
                'references_orig',
                'acquired_orig',
                'site_found_orig',
                # New fields
                'credit_line_orig',
                'region_orig',
                'sub_region_orig',
                'locale_orig',
                'excavation_orig',
                'museum_collection_orig',
                'style_orig',
                'culture_orig',
                'inscriptions_orig',
                'exhibitions_orig',
                'accession_date',
            ),
        }),
        ('English', {
            'classes': ('collapse',),
            'fields': (
                'title_en',
                'description_en',
                'department_en',
                'dimensions_en',
                'city_en',
                'object_date_en',
                'object_date_begin_en',
                'object_date_end_en',
                'period_en',
                'country_en',
                'object_type_en',
                'material_en',
                # 'references_en',
                'acquired_en',
                'site_found_en',
                # New fields
                'credit_line_en',
                'region_en',
                'sub_region_en',
                'locale_en',
                'excavation_en',
                'museum_collection_en',
                'style_en',
                'culture_en',
                'inscriptions_en',
                'exhibitions_en',
            ),
        }),
        ('Dutch', {
            'classes': ('collapse',),
            'fields': (
                'title_nl',
                'description_nl',
                'department_nl',
                'dimensions_nl',
                'city_nl',
                'object_date_nl',
                'object_date_begin_nl',
                'object_date_end_nl',
                'period_nl',
                'country_nl',
                'object_type_nl',
                'material_nl',
                # 'references_nl',
                'acquired_nl',
                'site_found_nl',
                # New fields
                'credit_line_nl',
                'region_nl',
                'sub_region_nl',
                'locale_nl',
                'excavation_nl',
                'museum_collection_nl',
                'style_nl',
                'culture_nl',
                'inscriptions_nl',
                'exhibitions_nl',
            ),
        }),
    )

    change_list_template = 'collection/admin/collection_change_list.html'

    class Media(object):
        """Custom media."""

        js = ('collection/collection_admin.js',)

    def get_queryset(self, request):
        """

        :param request:
        :return:
        """
        qs = super(ItemAdmin, self).get_queryset(request)
        qs = qs.prefetch_related('images')
        return qs

    def period_node_name(self, obj):
        """Readonly period name of associated period node

        :param obj:
        :return:
        :rtype: str
        """
        if obj.period_node:
            return obj.period_node.name_en
        else:
            return "No known period node"

    def admin_web_image_url(self, obj):
        """

        :return:
        """
        if obj.active and obj.web_image and obj.web_image.url:
            _web_image_url = obj.web_image.url
        else:
            _web_image_url = obj.web_image_url

        return format_html(
            '''
            <a href="{}" target="_blank">
                <img src="{}" style="width: 250px; height: auto;"/>
            </a>
            ''',
            _web_image_url,
            _web_image_url
        )

    admin_web_image_url.short_description = _("Web image URL preview")

    def _sync_collection(self, request, importer_uid=None):
        """Sync collection for the type (importer_uid) given.

        :param request:
        :param importer_uid:
        :return:
        """
        return do_import(importer_uid)

    def sync_collection(self, request):
        """Sync collection.

        :param request:
        :type request:
        :return:
        :rtype:
        """
        number_of_items = self._sync_collection(request)

        messages.info(
            request,
            _("Successfully imported {} items.").format(number_of_items)
        )
        return redirect('admin:muses_collection_item_changelist')

    def get_urls(self):
        urls = super(ItemAdmin, self).get_urls()
        my_urls = [
            url(r'^sync-collection/$',
                self.admin_site.admin_view(self.sync_collection),
                name='sync-collection')
        ]
        return my_urls + urls
