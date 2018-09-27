from collections import OrderedDict

from django.core import paginator as django_paginator

from django_elasticsearch_dsl_drf.pagination import PageNumberPagination, Page

from rest_framework.exceptions import NotFound
from rest_framework.response import Response

__all__ = (
    'CustomPageNumberPagination',
    'NoResultsPagination',
    'NoResultsPaginator',
)


class CustomPageNumberPagination(PageNumberPagination):
    """Custom page number pagination."""

    page_size = 30
    max_page_size = 10000
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data, extra_content=None):
        """Get paginated response.

        :param data:
        :return:
        """
        return Response(
            OrderedDict(
                self.get_paginated_response_context(
                    data,
                    extra_content=extra_content
                )
            )
        )

    def get_paginated_response_context(self, data, extra_content=None):
        __data = super(
            CustomPageNumberPagination,
            self
        ).get_paginated_response_context(data)
        __data.append(
            ('current_page', int(self.request.query_params.get('page', 1)))
        )
        __data.append(
            ('page_size', self.get_page_size(self.request))
        )

        if extra_content:
            for key, item in extra_content.items():
                __data.append(
                    (key, item)
                )

        try:
            view = self.request.parser_context['view']
            if view.extra_content:
                for key, item in view.extra_content.items():
                    __data.append(
                        (key, item)
                    )
        except Exception as err:
            pass

        return sorted(__data)


class NoResultsPaginator(django_paginator.Paginator):
    """Paginator for Elasticsearch."""

    def page(self, number):
        """Returns a Page object for the given 1-based page number.

        :param number:
        :return:
        """
        object_list = self.object_list[0:0].execute()
        __facets = getattr(object_list, 'aggregations', None)
        return self._get_page(object_list, number, self, facets=__facets)

    def _get_page(self, *args, **kwargs):
        """Get page.

        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)


class NoResultsPagination(CustomPageNumberPagination):

    django_paginator_class = NoResultsPaginator
    page_size = 1
    max_page_size = 1

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate a queryset.

        Paginate a queryset if required, either returning a page object,
        or `None` if pagination is not configured for this view.

        :param queryset:
        :param request:
        :param view:
        :return:
        """

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except django_paginator.InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
