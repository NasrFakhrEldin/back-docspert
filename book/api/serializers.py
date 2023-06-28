from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from book.models import Book, Page

Author = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["username"]


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["number", "content"]


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
    pages_length = serializers.SerializerMethodField()

    def get_pages_length(self, obj):
        return obj.pages.count()

    def get_pages(self, obj):
        number = self.context["request"].query_params.get("number")
        if number:
            page = obj.pages.filter(number=number).first()
            if not page:
                raise NotFound(detail="Page Not Found")
            return PageListSerializer(page).data
        return PageListSerializer(obj.pages.first()).data
