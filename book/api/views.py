from rest_framework import viewsets

from book.api.permissions import AuthorModifyOrReadOnly
from book.api.serializers import BookSerializer
from book.models import Book, Page


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AuthorModifyOrReadOnly]


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AuthorModifyOrReadOnly]
