from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class PetsListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 50

class PetListLOPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'

class PetListCPagination(CursorPagination):
    ordering = 'id'
    page_size = 2
    cursor_query_param = 'record'
