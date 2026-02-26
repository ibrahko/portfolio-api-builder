from django.contrib import admin

from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("file", "owner", "file_type", "size_bytes", "created_at")
    list_filter = ("file_type", "created_at")
    search_fields = ("file", "owner__username", "owner__email", "alt_text", "caption")
    autocomplete_fields = ("owner",)
    readonly_fields = ("size_bytes", "created_at")

    def get_readonly_fields(self, request, obj=None):
        # empêcher de modifier le fichier après upload (optionnel)
        ro = list(super().get_readonly_fields(request, obj))
        if obj:
            ro.append("file")
        return ro
