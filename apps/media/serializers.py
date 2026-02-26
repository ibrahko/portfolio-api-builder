from rest_framework import serializers

from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer principal pour un fichier média.
    Utilisé pour lister et uploader des fichiers (images, PDF, etc.).
    """

    owner_username = serializers.CharField(
        source="owner.username", read_only=True
    )

    class Meta:
        model = MediaFile
        fields = [
            "id",
            "owner",
            "owner_username",
            "file",
            "file_type",
            "alt_text",
            "caption",
            "size_bytes",
            "mime_type",
            "created_at",
        ]
        read_only_fields = (
            "id",
            "owner",
            "owner_username",
            "size_bytes",
            "mime_type",
            "created_at",
        )

    def create(self, validated_data):
        # Assigne toujours le propriétaire depuis le request.user
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["owner"] = request.user
        return super().create(validated_data)
