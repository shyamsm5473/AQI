"""
related_publication/admin.py
──────────────────────────────────────────────────────────────────────────────
Register the Publication model with the Django Admin so records can be
managed manually at /admin/ during development.
"""
from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display  = ("id", "year", "title", "authors", "publisher", "impact", "created_at")
    list_filter   = ("year", "publisher")
    search_fields = ("title", "authors", "journal")
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
