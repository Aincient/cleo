import operator
from django.conf import settings
from django_elasticsearch_dsl_drf.filter_backends.mixins import (
    FilterBackendMixin,
)
from django_elasticsearch_dsl_drf.utils import EmptySearch
from elasticsearch_dsl.query import Q
from rest_framework.filters import BaseFilterBackend

import six

from muses.user_account.serializers import UserSearchImageSerializer

__all__ = ('FindSimilarItemsByImageUploadBackend',)


class FindSimilarItemsByImageUploadBackend(
    BaseFilterBackend, FilterBackendMixin
):
    """Find similar items by image upload backend."""

    def get_user_search_image_object(self, request):
        """

        :param request:
        :return:
        """
        from muses.user_account.models import UserSearchImage
        user_search_image_id = request.query_params.get('user_search_image_id')
        if user_search_image_id:
            try:
                return UserSearchImage.objects.get(id=user_search_image_id)
            except Exception as err:
                pass
        return None

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
        # The reason this has been moved to function level is not circular
        # imports as you might think. It's that we have to open source the
        # project without open-sourcing model definitions (entire
        # ``naive_classification`` module) and thus to have the project
        # working certain parts have to be moved on function/method level.
        # It does not make the function, of course, but at least some parts of
        # the code will work.
        from muses.naive_classification.helpers_os import predict_image_path_dict
        from muses.naive_classification.definitions_os import synonyms_extended

        instance = self.get_user_search_image_object(request)

        if not request.query_params.get('user_search_image_id'):
            return queryset

        if not instance:
            return EmptySearch()

        image_path = instance.image.path
        conf = settings.MUSES_CONFIG['classification']['naive_classification']
        model_path = conf['model_path']

        prediction = predict_image_path_dict(
            image_path,
            model_path=model_path
        )

        top_matches = list(prediction.items())[0:3]
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
                        query = {'query': term, 'boost': (boost / (idx + 1))}
                    queries.append(
                        Q(
                            'match',
                            **{field_name: query}
                        )
                    )

            query = {'query': match[0], 'boost': (8 / (idx + 1))}
            queries.append(
                Q(
                    'match',
                    **{'classified_as': query}
                )
            )

        # Make sure only search results with images are shown
        queryset = queryset.query('exists', field='images')

        results = queryset.query(
            six.moves.reduce(operator.or_, queries)
        ).sort('_score')

        serializer = UserSearchImageSerializer(
            instance,
            context={'request': request}
        )

        view.extra_content = {
            'classified': list(prediction.items())[:5],
            'instance': serializer.data,
        }

        return results[0:200]
