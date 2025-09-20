from rest_framework.pagination import PageNumberPagination


class FormDataPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):

        page_number = request.data.get("page", 1)
        page_size = request.data.get("page_size", self.page_size)

        try:
            page_number = int(page_number)
        except (ValueError, TypeError):
            page_number = 1

        try:
            page_size = int(page_size)
        except (ValueError, TypeError):
            page_size = self.page_size

        self.page_size = page_size

        request.query_params._mutable = True
        request.query_params[self.page_query_param] = page_number
        request.query_params[self.page_size_query_param] = page_size
        request.query_params._mutable = False

        return super().paginate_queryset(queryset, request, view=view)