# Register your models here.
from django.contrib import admin

from .models import Book, Page


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("title", "author")
    list_filter = ("author",)
    search_fields = ("id", "title", "author")
    ordering = ("-created",)
    readonly_fields = ("created", "modified")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("id", "book__id", "book__title", "book__author")
    list_filter = ("book__id",)
    search_fields = ("book__id", "book__title", "book_author")
    ordering = ("-created",)
    readonly_fields = ("created", "modified")
