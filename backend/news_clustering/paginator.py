from rest_framework import pagination
from rest_framework.response import Response


class CustomPaginator(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.page_size,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
