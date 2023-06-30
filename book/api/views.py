from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)

from book.api.permissions import (
    AuthorModifyOrReadOnly,
    AuthorPageModifyOrReadOnly,
    IsAdminUserForObject,
)
from book.api.serializers import (
    BookDetailSerialzier,
    BookSerializer,
    PageSerializer,
    TokenObtainPairSerializer,
)
from book.models import Book, Page


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return BookSerializer
        return BookDetailSerialzier

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(vary_on_cookie)
    @action(methods=["get"], detail=False, name="Books by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Books are yours")

        books = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(books)

        if page is not None:
            serializer = BookSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = BookSerializer(books, many=True, context={"request": request})
        return Response(serializer.data)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [AuthorPageModifyOrReadOnly | IsAdminUserForObject]
