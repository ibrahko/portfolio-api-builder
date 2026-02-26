from django.contrib import admin

from .models import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "type", "title", "slug", "order", "is_visible")
    list_filter = ("type", "is_visible", "portfolio")
    search_fields = ("title", "slug", "portfolio__title")
    ordering = ("portfolio", "order")
    autocomplete_fields = ("portfolio",)
    prepopulated_fields = {"slug": ("title",)}
