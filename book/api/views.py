from rest_framework import viewsets

from book.api.permissions import AuthorModifyOrReadOnly, AuthorPageModifyOrReadOnly
from book.api.serializers import BookSerializer, PageSerializer
from book.models import Book, Page


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AuthorModifyOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [AuthorPageModifyOrReadOnly]
