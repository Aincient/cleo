import operator

from django.conf import settings
from django.db.models import Q

from django_elasticsearch_dsl import DocType, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

import six

from muses.collection.models.item import Item

from ..constants import VALUE_NOT_SPECIFIED
from .analyzers import (
    html_strip,
    html_strip_synonyms_en,
    html_strip_synonyms_nl,
)


__all__ = (
    'CollectionItemDocument',
    'INDEX',
)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    max_result_window=50000,  # Increase if needed
)


@INDEX.doc_type
class CollectionItemDocument(DocType):
    """Collection item document."""

    # ID
    id = fields.IntegerField(attr='id')

    record_number = KeywordField()

    inventory_number = KeywordField()

    api_url = KeywordField(
        index="not_analyzed"
    )

    web_url = KeywordField(
        index="not_analyzed"
    )

    # ********************************************************************
    # *************** Main data fields for search and filtering **********
    # ********************************************************************

    importer_uid = KeywordField(
        attr='importer_uid_indexing'
    )

    language_code_orig = KeywordField(
        attr='language_code_orig'
    )

    department = StringField(
        attr='department_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    # ********************************************************************
    # ***************************** English ******************************
    # ********************************************************************

    title_en = StringField(
        attr='title_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    description_en = StringField(
        attr='description_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    period_en = StringField(
        attr='period_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    period_1_en = fields.NestedField(
        attr='period_1_en_indexing',
        properties={
            'name': StringField(
                analyzer=html_strip_synonyms_en,
                fields={
                    'raw': KeywordField(),
                }
            ),
            'period_2_en': fields.NestedField(
                properties={
                    'name': StringField(
                        analyzer=html_strip_synonyms_en,
                        fields={
                            'raw': KeywordField(),
                        }
                    ),
                    'period_3_en': fields.NestedField(
                        properties={
                            'name': StringField(
                                analyzer=html_strip_synonyms_en,
                                fields={
                                    'raw': KeywordField(),
                                }
                            ),
                            'period_4_en': fields.NestedField(
                                properties={
                                    'name': StringField(
                                        analyzer=html_strip_synonyms_en,
                                        fields={
                                            'raw': KeywordField(),
                                        }
                                    )
                                }
                            )
                        }
                    )
                }
            )
        }
    )

    primary_object_type_en = StringField(
        attr='primary_object_type_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            'suggest': fields.CompletionField(),
        }
    )

    object_type_en = StringField(
        attr='object_type_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    object_type_detail_en = fields.TextField(
        attr='object_type_detail_en_indexing',
        index='no'
    )

    material_en = StringField(
        attr='material_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    material_detail_en = fields.TextField(
        attr='material_detail_en_indexing',
        index='no'
    )

    city_en = StringField(
        attr='city_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    country_en = StringField(
        attr='country_en_indexing',
        analyzer=html_strip_synonyms_en,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='english'),
            # 'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    references_en = fields.TextField(
        attr='references_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    acquired_en = fields.TextField(
        attr='acquired_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    site_found_en = fields.TextField(
        attr='site_found_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    reign_en = fields.TextField(
        attr='reign_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    keywords_en = fields.TextField(
        attr='keywords_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    dynasty_en = fields.TextField(
        attr='dynasty_en_indexing',
        index='no'
    )

    # New fields
    # To be shown on the detail page
    credit_line_en = fields.TextField(
        attr='credit_line_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    region_en = fields.TextField(
        attr='region_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    sub_region_en = fields.TextField(
        attr='sub_region_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    locale_en = fields.TextField(
        attr='locale_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    excavation_en = fields.TextField(
        attr='excavation_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    museum_collection_en = fields.TextField(
        attr='museum_collection_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    style_en = fields.TextField(
        attr='style_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    culture_en = fields.TextField(
        attr='culture_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    inscriptions_en = fields.TextField(
        attr='inscriptions_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    provenance_en = fields.TextField(
        attr='provenance_en_indexing',
        index='no'
    )

    # To be shown on the detail page
    exhibitions_en = fields.TextField(
        attr='exhibitions_en_indexing',
        index='no'
    )

    # ********************************************************************
    # ****************************** Dutch *******************************
    # ********************************************************************

    title_nl = StringField(
        attr='title_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    description_nl = StringField(
        attr='description_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    period_nl = StringField(
        attr='period_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    period_1_nl = fields.NestedField(
        attr='period_1_nl_indexing',
        properties={
            'name': StringField(
                analyzer=html_strip_synonyms_nl,
                fields={
                    'raw': KeywordField(),
                }
            ),
            'period_2_nl': fields.NestedField(
                properties={
                    'name': StringField(
                        analyzer=html_strip_synonyms_nl,
                        fields={
                            'raw': KeywordField(),
                        }
                    ),
                    'period_3_nl': fields.NestedField(
                        properties={
                            'name': StringField(
                                analyzer=html_strip_synonyms_nl,
                                fields={
                                    'raw': KeywordField(),
                                }
                            ),
                            'period_4_nl': fields.NestedField(
                                properties={
                                    'name': StringField(
                                        analyzer=html_strip_synonyms_nl,
                                        fields={
                                            'raw': KeywordField(),
                                        }
                                    )
                                }
                            )
                        }
                    )
                }
            )
        }
    )

    primary_object_type_nl = StringField(
        attr='primary_object_type_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            'suggest': fields.CompletionField(),
        }
    )

    object_type_nl = StringField(
        attr='object_type_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    object_type_detail_nl = fields.TextField(
        attr='object_type_detail_nl_indexing',
        index='no'
    )

    material_nl = StringField(
        attr='material_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    material_detail_nl = fields.TextField(
        attr='material_detail_nl_indexing',
        index='no'
    )

    city_nl = StringField(
        attr='city_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    country_nl = StringField(
        attr='country_nl_indexing',
        analyzer=html_strip_synonyms_nl,
        fields={
            'raw': KeywordField(),
            'natural': StringField(analyzer='dutch'),
            # 'suggest': fields.CompletionField(),
        }
    )

    # To be shown on the detail page
    keywords_nl = fields.TextField(
        attr='keywords_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    acquired_nl = fields.TextField(
        attr='acquired_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    site_found_nl = fields.TextField(
        attr='site_found_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    reign_nl = fields.TextField(
        attr='reign_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    references_nl = fields.TextField(
        attr='references_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    dynasty_nl = fields.TextField(
        attr='dynasty_nl_indexing',
        index='no'
    )

    # New fields
    # To be shown on the detail page
    credit_line_nl = fields.TextField(
        attr='credit_line_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    region_nl = fields.TextField(
        attr='region_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    sub_region_nl = fields.TextField(
        attr='sub_region_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    locale_nl = fields.TextField(
        attr='locale_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    excavation_nl = fields.TextField(
        attr='excavation_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    museum_collection_nl = fields.TextField(
        attr='museum_collection_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    style_nl = fields.TextField(
        attr='style_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    culture_nl = fields.TextField(
        attr='culture_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    inscriptions_nl = fields.TextField(
        attr='inscriptions_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    provenance_nl = fields.TextField(
        attr='provenance_nl_indexing',
        index='no'
    )

    # To be shown on the detail page
    exhibitions_nl = fields.TextField(
        attr='exhibitions_nl_indexing',
        index='no'
    )

    # ********************************************************************
    # ************************** Language independent ********************
    # ********************************************************************

    dimensions = StringField(
        attr='dimensions_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'natural': StringField(),
            # 'suggest': fields.CompletionField(),
        }
    )

    object_date_begin = StringField(
        attr='object_date_begin_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'natural': StringField(),
            # 'suggest': fields.CompletionField(),
        }
    )

    object_date_end = StringField(
        attr='object_date_end_indexing',
        analyzer=html_strip,
        fields={
            'raw': KeywordField(),
            'natural': StringField(),
            # 'suggest': fields.CompletionField(),
        }
    )

    location = fields.GeoPointField(attr='geo_location_indexing')

    # List of 32x32 PNG versions of the images. Full path to.
    images = fields.ListField(
        StringField(attr='images_indexing')
    )

    # List of image URLs.
    images_urls = fields.ListField(
        fields.ObjectField(
            attr='images_urls_indexing',
            properties={
                'th': KeywordField(index="not_analyzed"),
                'lr': KeywordField(index="not_analyzed"),
            }
        )
    )

    # Classified as by our AI
    classified_as = fields.ListField(
        StringField(
            attr='classified_as_indexing',
            fields={
                'raw': KeywordField(),
             }
        )
    )

    # Classified as 1st element
    classified_as_1 = StringField(
        attr='classified_as_1_indexing',
        fields={
            'raw': KeywordField(),
        }
    )

    # Classified as 2nd element
    classified_as_2 = StringField(
        attr='classified_as_2_indexing',
        fields={
            'raw': KeywordField(),
        }
    )

    # Classified as 3rd element
    classified_as_3 = StringField(
        attr='classified_as_3_indexing',
        fields={
            'raw': KeywordField(),
        }
    )

    # ********************************************************************
    # ************** Nested fields for search and filtering **************
    # ********************************************************************

    # # City object
    # country = fields.NestedField(
    #     properties={
    #         'name': StringField(
    #             analyzer=html_strip,
    #             fields={
    #                 'raw': KeywordField(),
    #                 'suggest': fields.CompletionField(),
    #             }
    #         ),
    #         'info': StringField(analyzer=html_strip),
    #         'location': fields.GeoPointField(attr='location_field_indexing'),
    #     }
    # )
    #
    # location = fields.GeoPointField(attr='location_field_indexing')

    class Meta(object):
        """Meta options."""

        model = Item  # The model associate with this DocType

    def get_queryset(self):
        """Filter out items that are not eligible for indexing."""
        qs = super(CollectionItemDocument, self).get_queryset()

        # qs = qs.select_related('period_node').prefetch_related('images')

        filters = []
        for field in ['title']:
            for language in ['en', 'nl']:
                filters.extend(
                    [
                        Q(**{"{}_{}__isnull".format(field, language): True}),
                        Q(**{"{}_{}__exact".format(field, language): ''}),
                    ]
                )

        if filters:
            qs = qs.exclude(
                six.moves.reduce(operator.or_, filters)
            )

        # We concatenate ``object_type`` and ``classification`` fields, after
        # cleaning them. Therefore, db-only checks don't work here.
        ids = []
        for item in qs:
            if not (
                item.object_type_en_indexing and item.object_type_nl_indexing
            ):
                ids.append(item.pk)

        return qs.exclude(id__in=ids)

    def prepare_department(self, instance):
        """Prepare department."""
        return instance.department_indexing \
            if instance.department_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_object_date_begin(self, instance):
        """Prepare material."""
        return instance.object_date_begin_indexing

    def prepare_object_date_end(self, instance):
        """Prepare material."""
        return instance.object_date_end_indexing

    # ********************************************************************
    # ***************************** English ******************************
    # ********************************************************************

    def prepare_material_en(self, instance):
        """Prepare material."""
        return instance.material_en_indexing \
            if instance.material_en_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_period_en(self, instance):
        """Prepare state."""
        return instance.period_en_indexing \
            if instance.period_en_indexing \
            else VALUE_NOT_SPECIFIED

    def prepare_dynasty_en(self, instance):
        """Prepare dynasty."""
        return instance.dynasty_en_indexing \
            if instance.dynasty_en_indexing \
            else VALUE_NOT_SPECIFIED

    def prepare_description_en(self, instance):
        """Prepare description."""
        return instance.description_en_indexing \
            if instance.description_en_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_city_en(self, instance):
        """Prepare city."""
        return instance.city_en_indexing \
            if instance.city_en_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_country_en(self, instance):
        """Prepare country."""
        return instance.country_en_indexing \
            if instance.country_en_indexing \
            else VALUE_NOT_SPECIFIED

    # ********************************************************************
    # ****************************** Dutch *******************************
    # ********************************************************************

    def prepare_material_nl(self, instance):
        """Prepare material."""
        return instance.material_nl_indexing \
            if instance.material_nl_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_period_nl(self, instance):
        """Prepare state."""
        return instance.period_nl_indexing \
            if instance.period_nl_indexing \
            else VALUE_NOT_SPECIFIED

    def prepare_dynasty_nl(self, instance):
        """Prepare dynasty."""
        return instance.dynasty_nl_indexing \
            if instance.dynasty_nl_indexing \
            else VALUE_NOT_SPECIFIED

    def prepare_description_nl(self, instance):
        """Prepare description."""
        return instance.description_nl_indexing \
            if instance.description_nl_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_city_nl(self, instance):
        """Prepare city."""
        return instance.city_nl_indexing \
            if instance.city_nl_indexing\
            else VALUE_NOT_SPECIFIED

    def prepare_country_nl(self, instance):
        """Prepare country."""
        return instance.country_nl_indexing \
            if instance.country_nl_indexing \
            else VALUE_NOT_SPECIFIED
