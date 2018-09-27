from django_elasticsearch_dsl_drf.constants import (
    ALL_LOOKUP_FILTERS_AND_QUERIES,
)
from django_elasticsearch_dsl_drf.filter_backends.mixins import (
    FilterBackendMixin,
)
from rest_framework.filters import BaseFilterBackend
from six import string_types

__all__ = ('NestedPeriodsBackend',)


class NestedPeriodsBackend(BaseFilterBackend, FilterBackendMixin):
    """Adds nesting to period."""

    faceted_search_param = 'nested_facet'

    def get_faceted_search_query_params(self, request):
        """Get faceted search query params.

        :param request: Django REST framework request.
        :type request: rest_framework.request.Request
        :return: List of search query params.
        :rtype: list
        """
        query_params = request.query_params.copy()
        return query_params.getlist(self.faceted_search_param, [])

    @classmethod
    def prepare_filter_fields(cls, view):
        """Prepare filter fields.
        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Filtering options.
        :rtype: dict
        """
        filter_fields = view.nested_filter_fields

        for field, options in filter_fields.items():
            if options is None or isinstance(options, string_types):
                filter_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in filter_fields[field]:
                filter_fields[field]['field'] = field

            if 'lookups' not in filter_fields[field]:
                filter_fields[field]['lookups'] = tuple(
                    ALL_LOOKUP_FILTERS_AND_QUERIES
                )

        return filter_fields

    def filter_queryset(self, request, queryset, view):
        """Filter the queryset.
        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        facets = self.get_faceted_search_query_params(request)

        if 'period_1_en' in facets:
            queryset \
                .aggs\
                .bucket('period_1_ens',
                        'nested',
                        path='period_1_en') \
                .bucket('period_1_en',
                        'terms',
                        field='period_1_en.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_2_ens',
                        'nested',
                        path='period_1_en.period_2_en') \
                .bucket('period_2_en',
                        'terms',
                        field='period_1_en.period_2_en.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_3_ens',
                        'nested',
                        path='period_1_en.period_2_en.period_3_en') \
                .bucket('period_3_en',
                        'terms',
                        field='period_1_en.period_2_en.period_3_en.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_4_ens',
                        'nested',
                        path='period_1_en.period_2_en.period_3_en.'
                             'period_4_en') \
                .bucket('period_4_en',
                        'terms',
                        field='period_1_en.period_2_en.period_3_en.'
                              'period_4_en.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        })

        if 'period_1_nl' in facets:
            queryset \
                .aggs\
                .bucket('period_1_nls',
                        'nested',
                        path='period_1_nl') \
                .bucket('period_1_nl_name',
                        'terms',
                        field='period_1_nl.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_2_nls',
                        'nested',
                        path='period_1_nl.period_2_nl') \
                .bucket('period_2_nl_name',
                        'terms',
                        field='period_1_nl.period_2_nl.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_3_nls',
                        'nested',
                        path='period_1_nl.period_2_nl.period_3_nl') \
                .bucket('period_3_nl_name',
                        'terms',
                        field='period_1_nl.period_2_nl.period_3_nl.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        }) \
                .bucket('period_4_nls',
                        'nested',
                        path='period_1_nl.period_2_nl.period_3_nl.'
                             'period_4_nl') \
                .bucket('period_4_nl_name',
                        'terms',
                        field='period_1_nl.period_2_nl.period_3_nl.'
                              'period_4_nl.name.raw',
                        size=20000,
                        order={
                            "_term": "asc"
                        })

        return queryset
