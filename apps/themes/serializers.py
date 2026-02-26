from rest_framework import serializers
from .models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "primary_color",
            "secondary_color",
            "background_color",
            "text_color",
            "font_family",
            "preview_image",
            "is_active",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")
