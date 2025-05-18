from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
     page_size = 6
     ordering = ('id')