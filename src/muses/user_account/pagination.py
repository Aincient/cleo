from rest_framework import pagination
from rest_framework.pagination import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

import six

__all__ = ('CustomPageNumberPagination',)


class CustomPageNumberPagination(pagination.PageNumberPagination):
    """Custom page number pagination."""

    page_size = 30
    max_page_size = 10000
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        #
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page.object_list)

    def get_paginated_response(self, data, extra_content=None):
        self.__data = data

        content = {}

        if extra_content and isinstance(extra_content, dict):
            content.update(extra_content)

        content.update({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': int(self.request.query_params.get('page', 1)),
            'page_size': self.get_page_size(self.request),
            'results': data,
        })

        return Response(content)
