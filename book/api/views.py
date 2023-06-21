from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from book.api.serializers import BookSerializer
from book.models import Book, Page


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
