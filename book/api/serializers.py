from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from book.models import Book, Page

Author = get_user_model()


class NestedPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_query_param = "pn"


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "username"]


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class BookDetailSerialzier(BookSerializer):
    pages = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_pages(self, instance):
        request = self.context.get("request")
        pages = instance.pages.all()

        if hasattr(request, "query_params"):
            pagination = NestedPageNumberPagination()
            paginated_pages = pagination.paginate_queryset(pages, request)
            page_serializer = PageListSerializer(paginated_pages, many=True)
            return pagination.get_paginated_response(page_serializer.data).data

        page_serializer = PageListSerializer(pages, many=True)
        return page_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["pages"] = self.get_pages(instance)
        return representation
