import csv
import operator
from django.conf import settings
from django.http import HttpResponse
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    # SUGGESTER_TERM,
    # SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    GeoSpatialFilteringFilterBackend,
    GeoSpatialOrderingFilterBackend,
    NestedFilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet

from elasticsearch_dsl.query import Q

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

import six

import tablib

from ..backends import (
    FindSimilarItemsByImageUploadBackend,
    NestedPeriodsBackend,
)
from ..documents import CollectionItemDocument
from ..pagination import CustomPageNumberPagination, NoResultsPagination
from ..serializers import (
    CollectionItemDocumentSerializer,
    CollectionItemDocumentDetailSerializer,
)
from ..throttling import SearchUserRateThrottle

__all__ = (
    'CollectionItemDocumentViewSet',
    'CollectionItemFacetsOnlyDocumentViewSet',
)


class CollectionItemDocumentViewSet(BaseDocumentViewSet):
    """The CollectionItemDocument view."""

    document = CollectionItemDocument
    serializer_class = CollectionItemDocumentSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        # GeoSpatialFilteringFilterBackend,
        # GeoSpatialOrderingFilterBackend,
        FindSimilarItemsByImageUploadBackend,
        NestedFilteringFilterBackend,
        NestedPeriodsBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]
    # pagination_class = LimitOffsetPagination
    # Define search fields
    search_fields = {
        # Language independent
        'record_number': {'boost': 8},
        'inventory_number': {'boost': 8},
        # English
        'title_en': {'boost': 3},
        'primary_object_type_en': {'boost': 3},
        'object_type_en': {'boost': 2},
        'description_en': {'boost': 2},
        'material_en': None,
        'city_en': None,
        'country_en': None,
        # Dutch
        'title_nl': {'boost': 3},
        'primary_object_type_nl': {'boost': 3},
        'object_type_nl': {'boost': 2},
        'description_nl': {'boost': 2},
        'material_nl': None,
        'city_nl': None,
        'country_nl': None,
    }

    # This structure will likely change in the upcoming versions of the
    # `django-elasticsearch-dsl-drf`. Have that in mind.
    search_nested_fields = {
        'period_1_en': ['period_1_en.name'],
        'period_1_en.period_2_en': ['period_1_en.period_2_en.name'],
        'period_1_en.period_2_en.period_3_en': [
            'period_1_en.period_2_en.period_3_en.name'
        ],
        'period_1_en.period_2_en.period_3_en.period_4_en': [
            'period_1_en.period_2_en.period_3_en.period_4_en.name'
        ],
    }

    # search_nested_fields = {
    #     'country': ['name'],
    # }

    permission_classes = (
        IsAuthenticated,
    )
    throttle_classes = (
        SearchUserRateThrottle,
    )
    scope_attr = 'search'

    # Define filtering fields
    filter_fields = {
        'id': None,
        'department': 'department.raw',
        'importer_uid': 'importer_uid',
        'classified_as': 'classified_as.raw',
        'classified_as_1': 'classified_as.raw',
        'classified_as_2': 'classified_as.raw',
        'classified_as_3': 'classified_as.raw',
        # English
        'title_en': 'title_en.natural',
        'description_en': 'description_en.natural',
        'primary_object_type_en': 'primary_object_type_en.raw',
        'object_type_en': 'object_type_en.raw',
        'material_en': 'material_en.raw',
        'period_en': 'period_en.raw',
        'city_en': 'city_en.raw',
        'country_en': 'country_en.raw',
        # Dutch
        'title_nl': 'title_nl.natural',
        'description_nl': 'description_nl.natural',
        'primary_object_type_nl': 'primary_object_type_nl.raw',
        'object_type_nl': 'object_type_nl.raw',
        'material_nl': 'material_nl.raw',
        'period_nl': 'period_nl.raw',
        'city_nl': 'city_nl.raw',
        'country_nl': 'country_nl.raw',
        'images': 'images',
    }
    # Nested filtering fields
    nested_filter_fields = {
        # English
        'period_1_en': {
            'field': 'period_1_en.name.raw',
            'path': 'period_1_en',
        },
        'period_2_en': {
            'field': 'period_1_en.period_2_en.name.raw',
            'path': 'period_1_en.period_2_en',
        },
        'period_3_en': {
            'field': 'period_1_en.period_2_en.period_3_en.name.raw',
            'path': 'period_1_en.period_2_en.period_3_en',
        },
        'period_4_en': {
            'field':
                'period_1_en.period_2_en.period_3_en.period_4_en.name.raw',
            'path': 'period_1_en.period_2_en.period_3_en.period_4_en',
        },
        # Dutch
        'period_1_nl': {
            'field': 'period_1_nl.name.raw',
            'path': 'period_1_nl',
        },
        'period_2_nl': {
            'field': 'period_1_nl.period_2_nl.name.raw',
            'path': 'period_1_nl.period_2_nl',
        },
        'period_3_nl': {
            'field': 'period_1_nl.period_2_nl.period_3_nl.name.raw',
            'path': 'period_1_nl.period_2_nl.period_3_nl',
        },
        'period_4_nl': {
            'field':
                'period_1_nl.period_2_nl.period_3_nl.period_4_nl.name.raw',
            'path': 'period_1_nl.period_2_nl.period_3_nl.period_4_nl',
        },
    }
    # Define geo-spatial filtering fields
    geo_spatial_filter_fields = {
        'location': {
            'lookups': [
                LOOKUP_FILTER_GEO_BOUNDING_BOX,
                LOOKUP_FILTER_GEO_DISTANCE,
                LOOKUP_FILTER_GEO_POLYGON,

            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        'score': '_score',
        'id': None,
        'title_en': 'title_en.raw',
        'title_nl': 'title_nl.raw',
        # 'country': 'country.name.raw',
    }
    # Define ordering fields
    geo_spatial_ordering_fields = {
        'location': None,
    }
    # Specify default ordering
    ordering = (
        '_score',
        'id',
        'title_en.raw',
    )

    # Note, that nested facets of fields `period_1_en` and `period_1_nl` is
    # implemented in the ``NestedPeriodsBackend`` filter backend.
    faceted_search_fields = {

        # ********************************************************************
        # ************************** Language independent ********************
        # ********************************************************************

        'department': 'department.raw',
        'importer_uid': {
            'field': 'importer_uid',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'language_code_orig': {
            'field': 'language_code_orig',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'object_date_begin': {
            'field': 'object_date_begin.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'object_date_end': {
            'field': 'object_date_end.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'classified_as': {
            'field': 'classified_as.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'classified_as_1': {
            'field': 'classified_as_1.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'classified_as_2': {
            'field': 'classified_as_2.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'classified_as_3': {
            'field': 'classified_as_3.raw',
            'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },

        # ********************************************************************
        # ***************************** English ******************************
        # ********************************************************************

        'title_en': {
            'field': 'title_en.raw',
            # 'enabled': True,
            "size": 20000,
            "order": {
                "_term": "asc"
            }
        },
        'description_en': {
            'field': 'description_en.raw',
            # 'enabled': True,
        },
        'material_en': {
            'field': 'material_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'primary_object_type_en': {
            'field': 'primary_object_type_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'object_type_en': {
            'field': 'object_type_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'city_en': {
            'field': 'city_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'country_en': {
            'field': 'country_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'period_en': {
            'field': 'period_en.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },

        # ********************************************************************
        # ****************************** Dutch *******************************
        # ********************************************************************

        'title_nl': {
            'field': 'title_nl.raw',
            # 'enabled': True
        },
        'description_nl': {
            'field': 'description_nl.raw',
            # 'enabled': True
        },
        'material_nl': {
            'field': 'material_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'primary_object_type_nl': {
            'field': 'primary_object_type_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'object_type_nl': {
            'field': 'object_type_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'city_nl': {
            'field': 'city_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'country_nl': {
            'field': 'country_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
        'period_nl': {
            'field': 'period_nl.raw',
            # 'enabled': True,
            'options': {
                "size": 20000,
                "order": {
                    "_term": "asc"
                }
            },
        },
    }

    # Suggester fields
    suggester_fields = {
        # 'title_en_suggest': {
        #     'field': 'title_en.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # },
        # 'object_type_en_suggest': {
        #     'field': 'object_type_en.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # },
        # 'material_suggest': {
        #     'field': 'material.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # },
        # 'country_suggest': {
        #     'field': 'country.name.suggest',
        #     'suggesters': [
        #         SUGGESTER_COMPLETION,
        #     ],
        # }
    }

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param args:
        :param kwargs:
        """
        super(CollectionItemDocumentViewSet, self).__init__(*args, **kwargs)
        self._extra_context = {}

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return CollectionItemDocumentDetailSerializer
        else:
            return CollectionItemDocumentSerializer

    def get_paginated_response(self, data, extra_content=None):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(
            data,
            extra_content=extra_content
        )

    @detail_route()
    def download(self, pk, *args, **kwargs):
        """Download a single item.

        :param pk:
        :return:
        """
        _format = self.request.query_params.get('docformat')
        obj = self.get_object()
        data = obj.to_dict()

        titles = [key for key in (data.keys())]
        values = [value for value in data.values()]

        export_data = tablib.Dataset(headers=titles)
        # Append titles for CSV export
        if _format != 'xlsx':
            export_data.append(titles)

        export_data.append(values)

        if _format == 'xlsx':
            response = HttpResponse(
                export_data.export('xlsx'),
                content_type='application/vnd.openxmlformats-'
                             'officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="{}.xlsx"' \
                                              ''.format(data['id'])
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="{}.csv"' \
                                              ''.format(data['id'])
            writer = csv.writer(response)
            writer.writerows(export_data)

        return response

    @list_route()
    def find_similar_items(self, request, *args, **kwargs):
        """Find similar items.

        :return:
        """
        from muses.naive_classification.helpers_os import predict_items
        from muses.naive_classification.definitions_os import synonyms_extended

        ids = request.query_params.getlist('id')
        qs = [
            item
            for item
            in self.get_queryset().filter('ids', **{'values': ids})[0:10]
        ]

        materials = []
        object_types = []
        periods = []

        for item in qs:
            materials.extend([i for i in item.material_en if i not in ['_', '']])
            object_types.extend([i for i in item.object_type_en if i not in ['_', '']])
            periods.extend([i for i in item.period_en if i not in ['_', '']])

        conf = settings.MUSES_CONFIG['classification']['naive_classification']
        model_path = conf['model_path']

        prediction = predict_items(
            qs,
            model_path=model_path
        )

        if not prediction:
            return Response()

        top_matches = list(prediction.items())[0:3]
        results_qs = CollectionItemDocument().search()

        # Make sure only search results with images are shown
        results_qs = results_qs.query('exists', field='images')

        queries = []
        for idx, match in enumerate(top_matches):
            search_terms = synonyms_extended.get(match[0])['synonyms']
            search_fields = synonyms_extended.get(match[0])['fields']
            for term in search_terms:
                for field in search_fields:
                    if isinstance(field, six.string_types):
                        field_name, boost = field, 1
                        query = {'query': term}
                    else:
                        field_name, boost = field
                        query = {'query': term, 'boost': int(boost / (idx + 1))}
                    queries.append(
                        Q(
                            'match',
                            **{field_name: query}
                        )
                    )

            query = {'query': match[0], 'boost': int(8 - idx)}
            queries.append(
                Q(
                    'match',
                    **{'classified_as': query}
                )
            )
        for material in materials:
            query = {'query': material, 'boost': 6}
            queries.append(
                Q(
                    'match',
                    **{'material_en': query}
                )
            )

        for object_type in object_types:
            query = {'query': object_type, 'boost': 8}
            queries.append(
                Q(
                    'match',
                    **{'object_type_en': query}
                )
            )

        for period in periods:
            query = {'query': period, 'boost': 4}
            queries.append(
                Q(
                    'match',
                    **{'period_en': query}
                )
            )

        results = results_qs.query(
            six.moves.reduce(operator.or_, queries)
        ).sort('_score').exclude('ids', **{'values': ids})

        # final_results = [res.to_dict() for res in results[0:200].execute()]
        final_results = results[0:200]

        page = self.paginate_queryset(final_results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                serializer.data,
                extra_content={
                    'classified': list(prediction.items())[:5],
                    'instances': [item.to_dict() for item in qs],
                }
            )

        serializer = self.get_serializer(final_results, many=True)
        return Response(serializer.data)


class CollectionItemFacetsOnlyDocumentViewSet(CollectionItemDocumentViewSet):
    """The CollectionItemDocument view for facets only."""

    pagination_class = NoResultsPagination
    filter_backends = [
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        NestedFilteringFilterBackend,
        NestedPeriodsBackend,
        DefaultOrderingFilterBackend,
    ]

    throttle_classes = []
