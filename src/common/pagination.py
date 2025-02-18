from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


def get_paginated_response_context(*, pagination_class, serializer_class, queryset, request, view, user_type=None):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        if user_type:
            serializer = serializer_class(page, many=True, user_type=user_type, context={'request': request, 'is_authenticated': request.user.is_authenticated})
        else:
            serializer = serializer_class(page, many=True,context={'request': request, 'is_authenticated': request.user.is_authenticated})
        return paginator.get_paginated_response(serializer.data)

    if user_type:
        serializer = serializer_class(queryset, many=True, user_type=user_type, context={'request': request, 'is_authenticated': request.user.is_authenticated})
    else:
        serializer = serializer_class(queryset, many=True, context={'request': request, 'is_authenticated': request.user.is_authenticated})

    return Response(data=serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 500

    def get_paginated_data(self, data):
        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next_link', self.get_next_link()),
            ('previous_link', self.get_previous_link()),
            ('next_offset', self.get_next_offset()),
            ('previous_offset', self.get_previous_offset()),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next_link', self.get_next_link()),
            ('previous_link', self.get_previous_link()),
            ('next_offset', self.get_next_offset()),
            ('previous_offset', self.get_previous_offset()),
            ('results', data)
        ]))

    def get_next_offset(self):
        if self.get_next_link() is not None:
            return self.offset + self.limit
        return None

    def get_previous_offset(self):
        if self.get_previous_link() is not None and self.offset > 0:
            return max(0, self.offset - self.limit)
        return None