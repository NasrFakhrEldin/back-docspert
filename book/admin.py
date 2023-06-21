from django.contrib import admin

from book.models import Book, Page


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    model = Page
