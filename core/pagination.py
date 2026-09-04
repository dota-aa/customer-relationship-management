from rest_framework.pagination import PageNumberPagination


class LargePagination(PageNumberPagination):
    page_query_param = 'page_num'
    page_size_query_param = 'limit'
    page_size = 100
    max_page_size = 1000


class MediumPagination(PageNumberPagination):
    page_query_param = 'page_num'
    page_size_query_param = 'limit'
    page_size = 20
    max_page_size = 100


class StandardPagination(PageNumberPagination):
    page_query_param = 'page_num'
    page_size_query_param = 'limit'
    page_size = 10
    max_page_size = 20
