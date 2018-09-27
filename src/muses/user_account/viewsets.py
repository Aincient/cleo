import csv
from collections import OrderedDict
import datetime
import operator

from django.conf import settings
from django.http import HttpResponse, JsonResponse

from elasticsearch_dsl.query import Q
import humanize

import six
import tablib

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework.response import Response

from muses.naive_classification.helpers_os import predict_image_path_dict
from muses.naive_classification.definitions_os import synonyms_extended

from muses.search_index.documents import CollectionItemDocument
from muses.search_index.serializers import CollectionItemDocumentSerializer
from muses.search_index.throttling import (
    get_scope_and_ident,
    get_rate,
    parse_rate,
    get_history,
    SearchUserRateThrottle,
)

from .models import UserCollectionItemFavourite, UserSearchImage
from .serializers import (
    UserCollectionItemFavouriteSerializer,
    UserApiUsageSerializer,
    UserSearchImageSerializer,
)
from .pagination import CustomPageNumberPagination

__all__ = (
    'UserCollectionItemFavouriteViewSet',
    'UserApiUsageViewSet',
    'UserSearchImageUploadViewSet',
    'UserSearchImageFindSimilarViewSet',
)


class UserCollectionItemFavouriteViewSet(ModelViewSet):
    """UserCollectionItemFavouriteViewSet."""

    serializer_class = UserCollectionItemFavouriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Get serializer class.

        :return:
        """
        serializer_class = super(
            UserCollectionItemFavouriteViewSet,
            self
        ).get_serializer_class()

        if self.action == 'show_indexes':
            return CollectionItemDocumentSerializer

        return serializer_class

    def get_queryset(self):
        """Get queryset.

        :return:
        """
        qs = UserCollectionItemFavourite \
            .objects \
            .filter(user=self.request.user)
        return qs

    def _get_indexed_data(self, request, with_fav_id=False):
        """Get indexed data.

        :param request:
        :return:
        """
        qs = self.get_queryset()
        favs = qs.values('id', 'collection_item_id')[:]
        cids = [fav['collection_item_id'] for fav in favs]
        keys = set()
        indexed_data = CollectionItemDocument \
            .search() \
            .filter('ids', **{'values': cids}) \
            .scan()
        data = []
        mapping = {fav['collection_item_id']: fav['id'] for fav in favs}
        for obj in indexed_data:
            _dict = obj.to_dict()
            if with_fav_id:
                _dict.update({'fav_id': mapping[_dict['id']]})
            data.append(_dict)
            keys = set(list(keys) + list(_dict.keys()))
        return data, keys

    @list_route()
    def show_indexes(self, request):
        """Show indexes."""
        data, keys = self._get_indexed_data(request, with_fav_id=True)
        return Response(
            OrderedDict(
                {
                    'count': len(data),
                    'page_size': 10000,
                    'current_page': 1,
                    'next': None,
                    'previous': None,
                    'results': data
                }
            )
        )

    @list_route()
    def export_all(self, request):
        """Export all items.

        :param request:
        :return:
        """
        _format = self.request.query_params.get('docformat')

        data, keys = self._get_indexed_data(request)

        # If no items to export, show an error.
        if not data:
            __response = JsonResponse(data={'error': "No items to export."})
            __response.status_code = 404
            return __response

        _titles = []
        for d in data:
            _titles.extend(list(d.keys()))
        _titles = list(set(_titles))

        # Create an empty data-set
        export_data = tablib.Dataset(headers=_titles)
        # Append titles for CSV export
        if _format != 'xlsx':
            export_data.append(_titles)

        # Add rows to the data-set
        for row in data:
            for key in keys:
                if key not in row:
                    row[key] = None

            _row = row.values()
            export_data.append(_row)

        if _format == 'xlsx':
            response = HttpResponse(
                export_data.export('xlsx'),
                content_type='application/vnd.openxmlformats-'
                             'officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="{}.xlsx"' \
                                              ''.format('favourites')
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename="{}.csv"' \
                                              ''.format('favourites')
            writer = csv.writer(response)
            writer.writerows(export_data)

        return response


class UserApiUsageViewSet(GenericViewSet):
    """User api usage view set."""

    serializer_class = UserApiUsageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """"""
        return []

    def list(self, *args, **kwargs):
        scope, ident = get_scope_and_ident(self.request)
        rate = get_rate(scope)
        num_requests, duration = parse_rate(rate)
        history = get_history(
            self.request,
            scope=scope,
            ident=ident
        )
        current_num_requests = len(history)

        if scope == settings.THROTTLE_NAME_SUBSCRIBED_USER:
            rate = None
            num_requests = self.request.user.account_settings.num_requests
            num_requests_left = num_requests
        else:
            num_requests_left = num_requests - current_num_requests

        serializer = UserApiUsageSerializer(
            data={
                'scope': scope,
                'rate': rate,
                'ident': ident,
                'num_requests_limit': num_requests,
                'duration_limit': humanize.naturaldelta(
                    datetime.timedelta(seconds=duration)
                ),
                'current_num_requests': current_num_requests,
                'num_requests_left': num_requests_left,
            }
        )
        serializer.is_valid()
        return Response(serializer.data)


class UserSearchImageUploadViewSet(ModelViewSet):
    """UserSearchImage upload view set."""

    serializer_class = UserSearchImageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Get queryset.

        :return:
        """
        qs = UserSearchImage \
            .objects \
            .filter(user=self.request.user)
        return qs


class UserSearchImageFindSimilarViewSet(ReadOnlyModelViewSet):
    """User search image find similar view set."""

    serializer_class = UserSearchImageSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (SearchUserRateThrottle,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        """Get queryset.

        :return:
        """
        qs = UserSearchImage \
            .objects \
            .filter(user=self.request.user)
        return qs

    def get_paginated_response(self, data, extra_content=None):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(
            data,
            extra_content=extra_content
        )

    def retrieve(self, request, *args, **kwargs):
        from muses.search_index.serializers import CollectionItemDocumentSerializer
        instance = self.get_object()
        image_path = instance.image.path
        conf = settings.MUSES_CONFIG['classification']['naive_classification']
        model_path = conf['model_path']

        prediction = predict_image_path_dict(
            image_path,
            model_path=model_path
        )

        top_matches = list(prediction.items())[0:3]
        qs = CollectionItemDocument().search()
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
                        query = {'query': term, 'boost': int(boost/(idx+1))}
                    queries.append(
                        Q(
                            'match',
                            **{field_name: query}
                        )
                    )

            query = {'query': match[0], 'boost': int(10 - idx)}
            queries.append(
                Q(
                    'match',
                    **{'classified_as_{}'.format(idx+1): query}
                )
            )

        results = qs.query(
            six.moves.reduce(operator.or_, queries)
        ).sort('_score')

        final_results = [res.to_dict() for res in results[0:200].execute()]

        serializer = self.get_serializer(instance)

        page = self.paginate_queryset(final_results)
        if page is not None:
            _serializer = CollectionItemDocumentSerializer(data=page, many=True)
            return self.get_paginated_response(
                _serializer.initial_data,
                extra_content={
                    'classified': list(prediction.items())[:5],
                    'instance': serializer.data,
                }
            )
        _serializer = CollectionItemDocumentSerializer(final_results, many=True)
        return Response(_serializer.initial_data)
