from django.contrib import admin

from book.models import Author, Book, Page


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    model = Page
