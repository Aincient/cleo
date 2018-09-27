from collections import OrderedDict

from elasticsearch_dsl.query import MoreLikeThis

from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents.collection_item import CollectionItemDocument, INDEX

__all__ = (
    'CollectionItemDocumentSerializer',
    'CollectionItemDocumentDetailSerializer',
)


class CollectionItemDocumentSerializer(DocumentSerializer):
    """Serializer for CollectionItemDocument."""

    class Meta(object):
        """Meta options."""

        document = CollectionItemDocument
        fields = (
            # Language independent
            'id',
            'importer_uid',
            'record_number',
            'inventory_number',
            'classified_as',
            'api_url',
            'web_url',
            'department',
            'dimensions',
            'object_date_begin',
            'object_date_end',
            'location',
            'images',
            'images_urls',
            # **********************
            # ******* English ******
            # **********************
            'title_en',
            'description_en',
            'period_en',
            'period_1_en',
            'primary_object_type_en',
            'object_type_en',
            'object_type_detail_en',
            'material_en',
            'material_detail_en',
            'city_en',
            'country_en',
            'keywords_en',
            'acquired_en',
            'site_found_en',
            'reign_en',
            'references_en',
            'dynasty_en',
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
            # **********************
            # ******** Dutch *******
            # **********************
            'title_nl',
            'description_nl',
            'period_nl',
            'primary_object_type_nl',
            'object_type_nl',
            'object_type_detail_nl',
            'material_nl',
            'material_detail_nl',
            'city_nl',
            'country_nl',
            'keywords_nl',
            'acquired_nl',
            'site_found_nl',
            'reign_nl',
            'references_nl',
            'dynasty_nl',
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
        )


class CollectionItemDocumentDetailSerializer(CollectionItemDocumentSerializer):
    """Detail view serializer for CollectionItemDocument."""

    related_items = serializers.SerializerMethodField()

    def get_related_items(self, obj):
        """Get related items.

        :param obj:
        :return:
        """
        max_query_terms = 25
        min_term_freq = 1,
        min_doc_freq = 1
        max_doc_freq = 25

        kwargs = {}

        if max_query_terms is not None:
            kwargs['max_query_terms'] = max_query_terms

        # if min_term_freq is not None:
        #     kwargs['min_term_freq'] = min_term_freq

        if min_doc_freq is not None:
            kwargs['min_doc_freq'] = min_doc_freq

        if max_doc_freq is not None:
            kwargs['max_doc_freq'] = max_doc_freq

        query = CollectionItemDocument().search()
        search = query.query(
            MoreLikeThis(
                fields=(
                    'title_en.natural',
                    'description_en.natural',
                ),
                like={
                    '_id': "{}".format(obj.id),
                    '_index': "{}".format(INDEX._name),
                    '_type': "{}".format(list(INDEX._mappings.keys())[0])
                },
                **kwargs
            )
        )
        related_items = []
        for __o in search:
            _id = int(__o.meta.id)
            related_items.append(
                OrderedDict([
                    ('id', _id),
                    ('images_urls', __o.images_urls._l_),
                    # English
                    ('title_en', __o.title_en._l_),
                    ('description_en', __o.description_en._l_),
                    # Dutch
                    ('title_nl', __o.title_nl._l_),
                    ('description_nl', __o.description_nl._l_),
                ])
            )

        return related_items
