from __future__ import absolute_import, unicode_literals

import json
import re
import logging

from django.contrib.gis.db.models import PointField
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_elasticsearch_dsl_drf.wrappers import dict_to_obj

from mptt.models import TreeForeignKey, TreeManyToManyField

from six import python_2_unicode_compatible

from muses.cached_api_calls.constants import (
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    POINT_REGEX,
)
from muses.search_index.constants import VALUE_NOT_SPECIFIED

from .constants import (
    MET_OBJECT_TYPE_EN_WHITELIST,
    MET_OBJECT_TYPE_NL_WHITELIST,
    MET_MATERIAL_EN_WHITELIST,
    MET_MATERIAL_NL_WHITELIST,
    OBJECT_TYPE_SYNONYMS_EN,
    OBJECT_TYPE_SYNONYMS_NL
)

__all__ = (
    'Item',
)


LOGGER = logging.getLogger(__name__)


def get_media_url(url):
    """Get media URL.

    :param url:
    :return:
    """
    _url = url.replace(settings.MEDIA_ROOT, '')
    if _url.startswith('/'):
        _url = _url[1:]
    return settings.MEDIA_URL + _url


@python_2_unicode_compatible
class Item(models.Model):
    """Collection item."""

    # *******************************************************************
    # ******************** Language independent data ********************
    # *******************************************************************
    importer_uid = models.CharField(
        max_length=255,
        verbose_name=_("Importer UID")
    )
    record_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Record number"),
        help_text=_("Record number")
    )
    inventory_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Inventory number"),
        help_text=_("Inventory number in the museum collection")
    )
    api_url = models.CharField(
        max_length=255,
        verbose_name=_("API item URL"),
        help_text=_("Link to original data in API")
    )
    web_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("External item URL"),
        help_text=_("Link to external data URL")
    )
    images = models.ManyToManyField(
        to='muses_collection.Image',
        verbose_name=_("Images"),
        # through='muses_collection.ItemImage'
    )
    geo_location = PointField(
        null=True,
        default='',
        blank=True,
        verbose_name=_("Geo coordinates"),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # *******************************************************************
    # ******************** Data translated into English *****************
    # *******************************************************************

    # TODO: Most likely, a suffix (defining the language) shall be added
    # to all searchable fields. For now leave as is, as we also need to
    # decide what do we do with the city and country fields. That's one of
    # the most important parts for now.

    title_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title (EN)"),
        help_text=_("Title of the object")
    )
    description_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description (EN)"),
        help_text=_("Description of the object")
    )
    department_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Department (EN)"),
        help_text=_("Department of the museum")
    )
    dimensions_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Dimensions (EN)"),
        help_text=_("Dimensions of the object")
    )
    city_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("City (EN)"),
    )
    object_date_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Object date (EN)"),
    )
    object_date_begin_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object date begin (EN)"),
    )
    object_date_end_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object date end (EN)"),
    )
    period_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Period (EN)"),
    )
    # state_province = models.CharField(
    #     max_length=255,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("State/province"),
    # )
    country_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Country (EN)"),
    )
    object_type_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object type (EN)"),
        help_text=_("Type of object")
    )
    material_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Material (EN)"),
        help_text=_("Material(s) of which the object is made")
    )
    dynasty_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Dynasty (EN)")
    )
    references_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("References (EN)"),
        help_text=_("References to this object in the professional literature")
    )
    acquired_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Acquired (EN)"),
        help_text=_("How the museum acquired the object")
    )
    site_found_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Site found (EN)"),
        help_text=_("Complete record of site where the object was found")
    )
    keywords_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Keywords (EN)"),
        help_text=_("Keywords")
    )
    reign_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Reign (EN)"),
        help_text=_("Reign")
    )
    classification_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Classification (EN)"),
        help_text=_("Classification")
    )

    # New fields
    credit_line_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Credit line (EN)"),
        help_text=_("Credit line")
    )
    region_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Region (EN)"),
        help_text=_("Region")
    )
    sub_region_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Sub region (EN)"),
        help_text=_("Sub region")
    )
    locale_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Locale (EN)"),
        help_text=_("Locale")
    )
    excavation_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Excavation (EN)"),
        help_text=_("Excavation")
    )
    museum_collection_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Museum collection (EN)"),
        help_text=_("Museum collection")
    )
    style_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Style (EN)"),
        help_text=_("Style")
    )
    culture_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Culture (EN)"),
        help_text=_("Culture")
    )
    inscriptions_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Inscriptions (EN)"),
        help_text=_("Inscriptions")
    )
    provenance_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Provenance (EN)"),
        help_text=_("Provenance")
    )
    exhibitions_en = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Exhibitions (EN)"),
        help_text=_("Exhibitions")
    )

    # *******************************************************************
    # ********************* Data translated into Dutch ******************
    # *******************************************************************

    # TODO: Most likely, a suffix (defining the language) shall be added
    # to all searchable fields. For now leave as is, as we also need to
    # decide what do we do with the city and country fields. That's one of
    # the most important parts for now.

    title_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title (NL)"),
        help_text=_("Title of the object")
    )
    description_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description (NL)"),
        help_text=_("Description of the object")
    )
    department_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Department (NL)"),
        help_text=_("Department of the museum")
    )
    dimensions_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Dimensions (NL)"),
        help_text=_("Dimensions of the object")
    )
    city_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("City (NL)"),
    )
    object_date_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Object date (NL)"),
    )
    object_date_begin_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object date begin (NL)"),
    )
    object_date_end_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object date end (NL)"),
    )
    period_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Period (NL)"),
    )
    # state_province = models.CharField(
    #     max_length=255,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("State/province"),
    # )
    country_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Country (NL)"),
    )
    object_type_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Object type (NL)"),
        help_text=_("Type of object")
    )
    material_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Material (NL)"),
        help_text=_("Material(s) of which the object is made")
    )
    dynasty_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Dynasty (NL)")
    )
    references_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("References (NL)"),
        help_text=_("References to this object in the professional literature")
    )
    acquired_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Acquired (NL)"),
        help_text=_("How the museum acquired the object")
    )
    site_found_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Site found (NL)"),
        help_text=_("Complete record of site where the object was found")
    )
    keywords_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Keywords (NL)"),
        help_text=_("Keywords")
    )
    reign_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Reign (NL)"),
        help_text=_("Reign")
    )
    classification_nl = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Classification (NL)"),
        help_text=_("Classification")
    )

    # New fields
    credit_line_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Credit line (NL)"),
        help_text=_("Credit line")
    )
    region_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Region (NL)"),
        help_text=_("Region")
    )
    sub_region_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Sub region (NL)"),
        help_text=_("Sub region")
    )
    locale_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Locale (NL)"),
        help_text=_("Locale")
    )
    excavation_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Excavation (NL)"),
        help_text=_("Excavation")
    )
    museum_collection_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Museum collection (NL)"),
        help_text=_("Museum collection")
    )
    style_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Style (NL)"),
        help_text=_("Style")
    )
    culture_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Culture (NL)"),
        help_text=_("Culture")
    )
    inscriptions_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Inscriptions (NL)"),
        help_text=_("Inscriptions")
    )
    provenance_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Provenance (NL)"),
        help_text=_("Provenance")
    )
    exhibitions_nl = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Exhibitions (NL)"),
        help_text=_("Exhibitions")
    )

    # *******************************************************************
    # ******************** Original data as imported ********************
    # *******************************************************************

    language_code_orig = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name=_("Language code of the original")
    )

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
    department_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original department"),
        help_text=_("Department of the museum")
    )
    dimensions_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original dimensions"),
        help_text=_("Dimensions of the object")
    )
    city_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original city"),
    )
    object_date_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original object date"),
    )
    object_date_begin_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original object date begin"),
    )
    object_date_end_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original object date end"),
    )
    period_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original period"),
    )
    dynasty_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original dynasty"),
    )
    # state_province_orig = models.CharField(
    #     max_length=255,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("Original state/province"),
    # )
    country_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original country"),
    )
    object_type_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original object type"),
        help_text=_("Type of object")
    )
    material_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original material"),
        help_text=_("Material(s) of which the object is made")
    )
    references_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original references"),
        help_text=_("References to this object in the professional literature")
    )
    acquired_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Original acquired"),
        help_text=_("How the museum acquired the object")
    )
    site_found_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Original site found"),
        help_text=_("Complete record of site where the object was found")
    )
    keywords_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Keywords"),
        help_text=_("Keywords")
    )
    reign_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Reign"),
        help_text=_("Reign")
    )
    classification_orig = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Classification"),
        help_text=_("Classification")
    )
    period_node = TreeForeignKey(
        'Period',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Period tree node"),
        help_text=_("The database period that is related to this object")
    )
    classified_as = models.TextField(
        verbose_name=_("Classified as"),
        null=True,
        blank=True,
        help_text=_("How this object was classified by our AI.")
    )

    # New fields
    credit_line_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Credit line")
    )
    region_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Region")
    )
    sub_region_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Sub region"),
    )
    locale_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Locale"),
    )
    excavation_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Excavation"),
    )
    museum_collection_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Collection"),
    )
    style_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Style"),
    )
    culture_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Culture"),
    )
    inscriptions_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Inscriptions"),
    )
    provenance_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Provenance"),
    )
    accession_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Accession date"),
    )
    exhibitions_orig = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Exhibitions"),
    )

    class Meta(object):
        """Meta options."""

        ordering = ["id"]
        unique_together = (
            (
                'importer_uid',
                'record_number',
                'inventory_number',
                # 'api_url',
                # 'web_url',
                # 'title_orig',
                # 'dimensions_orig',
                # 'period_orig',
                # 'object_date_begin_orig',
                # 'object_date_end_orig',
                # 'object_type_orig',
                # 'material_orig',
            ),
        )

    def __str__(self):
        return str(self.title_orig)

    def _split_field_value(self, field, delimiters='; |, |\*|\n| ; |;'):
        """Split field value.

        :param field:
        :return:
        """
        if field:
            split_value = [_it.strip()
                           for _it
                           in re.split(delimiters, field)
                           if _it.strip()]
            if split_value:
                return split_value
            else:
                return [field]

    def _clean_field_value(self, field):
        try:
            clean_field = re.sub(" ?\(?\? ?\)?| \( ?\)|\|.*|\(.*?\)|\(\? \)", "", field).strip()
            if clean_field:
                return clean_field.capitalize() \
                    if clean_field.islower() \
                    else clean_field
            else:
                return field
        except:
            return field

    @property
    def importer_uid_indexing(self):
        """Importer UID for indexing."""
        return self.importer_uid

    @property
    def department_indexing(self):
        """Department for indexing."""
        return self.department_orig

    @property
    def classified_as_indexing(self):
        """Classified as for indexing."""
        if self.classified_as:
            try:
                classified_as = json.loads(self.classified_as)
                return [item[0] for item in classified_as][:3]
            except json.decoder.JSONDecodeError as err:
                _classified_as = self.classified_as.replace("'", '"') \
                                                   .replace('(', '[') \
                                                   .replace(')', ']')
                classified_as = json.loads(_classified_as)
                return [item[0] for item in classified_as][:3]
            except Exception as err:
                pass

        return []

    @property
    def classified_as_1_indexing(self):
        """Classified as 1st for indexing."""
        if self.classified_as_indexing:
            return self.classified_as_indexing[0]

        return VALUE_NOT_SPECIFIED

    @property
    def classified_as_2_indexing(self):
        """Classified as 2nd for indexing."""
        if len(self.classified_as_indexing) > 1:
            return self.classified_as_indexing[1]

        return VALUE_NOT_SPECIFIED

    @property
    def classified_as_3_indexing(self):
        """Classified as 3rd for indexing."""
        if len(self.classified_as_indexing) > 2:
            return self.classified_as_indexing[2]

        return VALUE_NOT_SPECIFIED

    def _period_node_indexing(self, lang):
        """Period node for indexing."""
        counter = 0
        tree_dict = {}
        parent = None

        if self.period_node:
            tree = [
                '{}_{}'.format(
                    str(el.id).zfill(4), getattr(el, 'name_{}'.format(lang))
                )
                for el
                in self.period_node.get_ancestors(include_self=True)
            ]
            tree.pop(0)

            # if len(tree) > 2:
            #     tree = tree[:2]

            for counter, item in enumerate(tree):
                if counter == 0:
                    tree_dict['period_1_{}'.format(lang)] = {'name': item}
                    parent = tree_dict['period_1_{}'.format(lang)]
                else:
                    parent['period_{}_{}'.format(counter + 1, lang)] = {
                        'name': item
                    }
                    parent = parent['period_{}_{}'.format(counter + 1, lang)]

        # return tree_dict

        if counter > 0:
            counter += 1

        # Filling the missing gaps, since we need that.
        while counter < 4:
            if counter == 0:
                tree_dict['period_1_{}'.format(lang)] = {
                    'name': VALUE_NOT_SPECIFIED
                }
                parent = tree_dict['period_1_{}'.format(lang)]
            else:
                parent['period_{}_{}'.format(counter + 1, lang)] = {
                    'name': VALUE_NOT_SPECIFIED
                }
                parent = parent['period_{}_{}'.format(counter + 1, lang)]
            counter += 1

        if tree_dict:
            return tree_dict['period_1_{}'.format(lang)]

        return {}

    # ********************************************************************
    # ***************************** English ******************************
    # ********************************************************************

    @property
    def department_en_indexing(self):
        """Department for indexing."""
        return self.department_en

    @property
    def primary_object_type_en_indexing(self):
        """Primary object type for indexing."""
        return self._clean_field_value(self.object_type_en_indexing[0]) \
            if self.object_type_en_indexing \
            else VALUE_NOT_SPECIFIED

    @property
    def title_en_indexing(self):
        """Title for indexing."""
        return self._split_field_value(self.title_en)

    @property
    def object_type_en_indexing(self):
        """Object type for indexing."""
        object_type_en = self._split_field_value(self.object_type_en)
        if object_type_en is None:
            object_type_en = []

        _classification_en = self._split_field_value(self.classification_en)
        if _classification_en is None:
            _classification_en = []

        classification_en = [
            _item
            for _item in _classification_en
            if _item in MET_OBJECT_TYPE_EN_WHITELIST
        ]

        object_type_clean = [self._clean_field_value(val)
                             for val in (object_type_en + classification_en)
                             if val not in ['||', '|']]

        object_type_synonyms = [
            OBJECT_TYPE_SYNONYMS_EN[object_type.lower()]
            for object_type in object_type_clean
            if object_type.lower() in OBJECT_TYPE_SYNONYMS_EN
            and OBJECT_TYPE_SYNONYMS_EN[object_type.lower()] != 'Do not use'
        ]

        return object_type_synonyms\
            if object_type_synonyms \
            else VALUE_NOT_SPECIFIED

    @property
    def object_type_detail_en_indexing(self):
        """Object type for indexing. To be shown on detail page."""
        object_type_en = self._split_field_value(self.object_type_en)
        if object_type_en is None:
            object_type_en = []

        classification_en = self._split_field_value(self.classification_en)
        if classification_en is None:
            classification_en = []

        return object_type_en + classification_en

    @property
    def description_en_indexing(self):
        """Description for indexing."""
        if not self.importer_uid == 'brooklynmuseum_org':
            return self._split_field_value(self.description_en)
        return VALUE_NOT_SPECIFIED

    @property
    def material_en_indexing(self):
        """Material type for indexing."""
        material_en = []
        clean = self._clean_field_value(self.material_en)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        for item in val:
            match = [re.search(material, item, flags=re.I) for material in MET_MATERIAL_EN_WHITELIST]
            if any(x is not None for x in match):
                material_en.append(
                    MET_MATERIAL_EN_WHITELIST[next((i for i, v in enumerate(match) if v is not None), -1)].capitalize()
                )
        return material_en

    @property
    def material_detail_en_indexing(self):
        """Material type for indexing. To be shown on detail page."""
        clean = self._clean_field_value(self.material_en)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def period_en_indexing(self):
        """Period for indexing."""
        return self._split_field_value(self.period_en)

    @property
    def period_1_en_indexing(self):
        return dict_to_obj(self._period_node_indexing('en'))

    @property
    def city_en_indexing(self):
        """City for indexing."""
        clean = self._clean_field_value(self.city_en)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| ; | or | and | Or|,|;')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def country_en_indexing(self):
        """Country for indexing."""
        clean = self._clean_field_value(self.country_en)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| ; | or | and | Or')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def keywords_en_indexing(self):
        """Keywords for indexing. To be shown on detail page."""
        clean = self._clean_field_value(self.keywords_en)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def acquired_en_indexing(self):
        """Acquired for indexing. To be shown on detail page."""
        if not self.acquired_en:
            return VALUE_NOT_SPECIFIED
        return self.acquired_en

    @property
    def site_found_en_indexing(self):
        """Acquired for indexing. To be shown on detail page."""
        if not self.site_found_en:
            return VALUE_NOT_SPECIFIED
        return self.site_found_en

    @property
    def reign_en_indexing(self):
        """Reign for indexing. To be shown on detail page."""
        if not self.reign_en:
            return VALUE_NOT_SPECIFIED
        return self.reign_en

    @property
    def references_en_indexing(self):
        """References for indexing. To be shown on detail page."""
        if not self.references_orig:
            return VALUE_NOT_SPECIFIED
        return self.references_orig

    @property
    def dynasty_en_indexing(self):
        """Dynasty for indexing. To be shown on detail page."""
        if not self.dynasty_en:
            return VALUE_NOT_SPECIFIED
        return self.dynasty_en

    # New fields
    @property
    def credit_line_en_indexing(self):
        """credit_line_en for indexing. To be shown on detail page."""
        if not self.credit_line_en:
            return VALUE_NOT_SPECIFIED
        return self.credit_line_en

    @property
    def region_en_indexing(self):
        """region_en for indexing. To be shown on detail page."""
        if not self.region_en:
            return VALUE_NOT_SPECIFIED
        return self.region_en

    @property
    def sub_region_en_indexing(self):
        """sub_region_en for indexing. To be shown on detail page."""
        if not self.sub_region_en:
            return VALUE_NOT_SPECIFIED
        return self.sub_region_en

    @property
    def locale_en_indexing(self):
        """locale_en for indexing. To be shown on detail page."""
        if not self.locale_en:
            return VALUE_NOT_SPECIFIED
        return self.locale_en

    @property
    def locus_en_indexing(self):
        """locus_en for indexing. To be shown on detail page."""
        if self.importer_uid == 'brooklynmuseum_org':
            if self.description_en:
                return self.description_en
        return VALUE_NOT_SPECIFIED

    @property
    def excavation_en_indexing(self):
        """excavation_en for indexing. To be shown on detail page."""
        if not self.excavation_en:
            return VALUE_NOT_SPECIFIED
        return self.excavation_en

    @property
    def museum_collection_en_indexing(self):
        """museum_collection_en for indexing. To be shown on detail page."""
        if not self.museum_collection_en:
            return VALUE_NOT_SPECIFIED
        return self.museum_collection_en

    @property
    def style_en_indexing(self):
        """style_en for indexing. To be shown on detail page."""
        if not self.style_en:
            return VALUE_NOT_SPECIFIED
        return self.style_en

    @property
    def culture_en_indexing(self):
        """Dynasty for indexing. To be shown on detail page."""
        if not self.culture_en:
            return VALUE_NOT_SPECIFIED
        return self.culture_en

    @property
    def inscriptions_en_indexing(self):
        """inscriptions_en for indexing. To be shown on detail page."""
        if not self.inscriptions_en:
            return VALUE_NOT_SPECIFIED
        return self.inscriptions_en

    @property
    def provenance_en_indexing(self):
        """provenance_en for indexing. To be shown on detail page."""
        if not self.provenance_en:
            return VALUE_NOT_SPECIFIED
        return self.provenance_en

    @property
    def exhibitions_en_indexing(self):
        """exhibitions_en for indexing. To be shown on detail page."""
        if not self.exhibitions_en:
            return VALUE_NOT_SPECIFIED
        return self._split_field_value(self.exhibitions_en)

    # ********************************************************************
    # ****************************** Dutch *******************************
    # ********************************************************************

    @property
    def department_nl_indexing(self):
        """Department for indexing."""
        return self.department_nl

    @property
    def primary_object_type_nl_indexing(self):
        """Primary object type for indexing."""
        return self._clean_field_value(self.object_type_nl_indexing[0]) \
            if self.object_type_nl_indexing \
            else VALUE_NOT_SPECIFIED

    @property
    def title_nl_indexing(self):
        """Title for indexing."""
        return self._split_field_value(self.title_nl)

    @property
    def object_type_nl_indexing(self):
        """Object type for indexing."""
        object_type_nl = self._split_field_value(self.object_type_nl)
        if object_type_nl is None:
            object_type_nl = []

        _classification_nl = self._split_field_value(self.classification_nl)
        if _classification_nl is None:
            _classification_nl = []

        classification_nl = [
            _item
            for _item in _classification_nl
            if _item in MET_OBJECT_TYPE_NL_WHITELIST
        ]

        object_type_clean = [self._clean_field_value(val)
                             for val in (object_type_nl + classification_nl)
                             if val not in ['||', '|']]

        object_type_synonyms = [
            OBJECT_TYPE_SYNONYMS_NL[object_type.lower()]
            for object_type in object_type_clean
            if object_type.lower() in OBJECT_TYPE_SYNONYMS_NL
            and OBJECT_TYPE_SYNONYMS_NL[object_type.lower()] != 'Do not use'
            ]

        return object_type_synonyms \
            if object_type_synonyms \
            else VALUE_NOT_SPECIFIED

    @property
    def object_type_detail_nl_indexing(self):
        """Object type for indexing. To be shown on detail page."""
        object_type_nl = self._split_field_value(self.object_type_nl)
        if object_type_nl is None:
            object_type_nl = []

        classification_nl = self._split_field_value(self.classification_nl)
        if classification_nl is None:
            classification_nl = []

        return object_type_nl + classification_nl

    @property
    def description_nl_indexing(self):
        """Description for indexing."""
        return self._split_field_value(self.description_nl)

    @property
    def material_nl_indexing(self):
        """Material type for indexing."""
        material_nl = []
        clean = self._clean_field_value(self.material_nl)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        for item in val:
            match = [re.search(material, item, flags=re.I) for material in MET_MATERIAL_NL_WHITELIST]
            if any(x is not None for x in match):
                material_nl.append(
                    MET_MATERIAL_NL_WHITELIST[next((i for i, v in enumerate(match) if v is not None), -1)].capitalize()
                )
        return material_nl

    @property
    def material_detail_nl_indexing(self):
        """Material type for indexing. To be shown on detail page."""
        clean = self._clean_field_value(self.material_nl)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def period_nl_indexing(self):
        """Period for indexing."""
        return self._split_field_value(self.period_nl)

    @property
    def period_1_nl_indexing(self):
        return dict_to_obj(self._period_node_indexing('nl'))

    @property
    def city_nl_indexing(self):
        """City for indexing."""
        clean = self._clean_field_value(self.city_nl)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| ; | of | en | Of|,|;')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def country_nl_indexing(self):
        """Country for indexing."""
        clean = self._clean_field_value(self.country_nl)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| ; | of | en | Of')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def keywords_nl_indexing(self):
        """Keywords for indexing. To be shown on detail page."""
        clean = self._clean_field_value(self.keywords_nl)
        val = self._split_field_value(clean, delimiters='; |, |\*|\n| of')
        if not val:
            return VALUE_NOT_SPECIFIED
        return val

    @property
    def acquired_nl_indexing(self):
        """Acquired for indexing. To be shown on detail page."""
        if not self.acquired_nl:
            return VALUE_NOT_SPECIFIED
        return self.acquired_nl

    @property
    def site_found_nl_indexing(self):
        """Acquired for indexing. To be shown on detail page."""
        if not self.site_found_nl:
            return VALUE_NOT_SPECIFIED
        return self.site_found_nl

    @property
    def reign_nl_indexing(self):
        """Reign for indexing. To be shown on detail page."""
        if not self.reign_nl:
            return VALUE_NOT_SPECIFIED
        return self.reign_nl

    @property
    def references_nl_indexing(self):
        """References for indexing. To be shown on detail page."""
        if not self.references_orig:
            return VALUE_NOT_SPECIFIED
        return self.references_orig

    @property
    def dynasty_nl_indexing(self):
        """Dynasty for indexing. To be shown on detail page."""
        if not self.dynasty_nl:
            return VALUE_NOT_SPECIFIED
        return self.dynasty_nl

    # New fields
    @property
    def credit_line_nl_indexing(self):
        """credit_line_nl for indexing. To be shown on detail page."""
        if not self.credit_line_nl:
            return VALUE_NOT_SPECIFIED
        return self.credit_line_nl

    @property
    def region_nl_indexing(self):
        """region_nl for indexing. To be shown on detail page."""
        if not self.region_nl:
            return VALUE_NOT_SPECIFIED
        return self.region_nl

    @property
    def sub_region_nl_indexing(self):
        """sub_region_nl for indexing. To be shown on detail page."""
        if not self.sub_region_nl:
            return VALUE_NOT_SPECIFIED
        return self.sub_region_nl

    @property
    def locale_nl_indexing(self):
        """locale_nl for indexing. To be shown on detail page."""
        if not self.locale_nl:
            return VALUE_NOT_SPECIFIED
        return self.locale_nl

    @property
    def excavation_nl_indexing(self):
        """excavation_nl for indexing. To be shown on detail page."""
        if not self.excavation_nl:
            return VALUE_NOT_SPECIFIED
        return self.excavation_nl

    @property
    def museum_collection_nl_indexing(self):
        """museum_collection_nl for indexing. To be shown on detail page."""
        if not self.museum_collection_nl:
            return VALUE_NOT_SPECIFIED
        return self.museum_collection_nl

    @property
    def style_nl_indexing(self):
        """style_nl for indexing. To be shown on detail page."""
        if not self.style_nl:
            return VALUE_NOT_SPECIFIED
        return self.style_nl

    @property
    def culture_nl_indexing(self):
        """culture_nl for indexing. To be shown on detail page."""
        if not self.culture_nl:
            return VALUE_NOT_SPECIFIED
        return self.culture_nl

    @property
    def inscriptions_nl_indexing(self):
        """inscriptions_nl for indexing. To be shown on detail page."""
        if not self.inscriptions_nl:
            return VALUE_NOT_SPECIFIED
        return self.inscriptions_nl

    @property
    def provenance_nl_indexing(self):
        """provenance_nl for indexing. To be shown on detail page."""
        if not self.provenance_nl:
            return VALUE_NOT_SPECIFIED
        return self.provenance_nl

    @property
    def exhibitions_nl_indexing(self):
        """exhibitions_nl for indexing. To be shown on detail page."""
        if not self.exhibitions_nl:
            return VALUE_NOT_SPECIFIED
        return self._split_field_value(self.exhibitions_nl)

    # ********************************************************************
    # ************************** Language independent ********************
    # ********************************************************************

    @property
    def object_date_indexing(self):
        """Object date for indexing."""
        return self._split_field_value(self.object_date_orig)

    @property
    def object_date_begin_indexing(self):
        """Object date begin for indexing."""
        return self.object_date_begin_orig

    @property
    def object_date_end_indexing(self):
        """Object date for indexing."""
        return self.object_date_end_orig

    @property
    def dimensions_indexing(self):
        """Dimensions for indexing."""
        return self.dimensions_orig

    @property
    def images_indexing(self):
        """Images (used in indexing).

        :return:
        """
        val = []

        for _im in self.images \
                .all() \
                .filter(active=True) \
                .order_by('-primary', 'created'):

            try:
                if _im.image and _im.image.url:
                    val.append(_im.image_ml.path)
            except IOError as err:
                LOGGER.error(err)
                LOGGER.error("Image details: id {}".format(_im.id))

        return val

    @property
    def images_urls_indexing(self):
        """Images URLs (used in indexing).

        :return:
        """
        val = []

        for _im in self.images \
                .all() \
                .filter(active=True) \
                .order_by('-primary', 'created'):

            try:
                if _im.image and _im.image.url:
                    val.append(
                        {
                            'th': get_media_url(_im.image_sized.path),
                            'lr': get_media_url(_im.image_large.path),
                        }
                    )
            except IOError as err:
                LOGGER.error(err)
                LOGGER.error("Image details: id {}".format(_im.id))

        if val:
            return val

        return [{}]

    @property
    def coordinates(self):
        """Coordinates usable on the map."""
        if self.geo_location:
            lat, lng = self.geo_location.tuple
            return str(lat), str(lng)
        return None

    @property
    def coordinates_str(self):
        """Coordinates string."""
        lat, lng = self.coordinates
        if lat and lng:
            return "{0},{1}".format(lat, lng)

    @property
    def geo_location_indexing(self):
        """Location for indexing.
        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        coordinates = self.coordinates
        lat, lon = DEFAULT_LATITUDE, DEFAULT_LONGITUDE
        if coordinates:
            lat, lon = coordinates
        return {
            'lat': lat,
            'lon': lon,
        }
