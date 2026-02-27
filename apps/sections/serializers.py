from rest_framework import serializers
from .models import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "id",
            "portfolio",
            "type",
            "title",
            "slug",
            "is_visible",
            "order",
            "settings",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_settings(self, value):
        # Si le frontend envoie explicitement null → on remplace par {}
        if value is None:
            return {}
        return value