from rest_framework import serializers

from .models import NotificationPreference, ContactMessage, EmailLog

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = NotificationPreference
        fields = [
            "id",
            "user",
            "user_email",
            "receive_contact_emails",
            "receive_product_updates",
        ]
        read_only_fields = ("id", "user", "user_email")

    def create(self, validated_data):
        # On force l'user depuis le contexte (le request.user)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # L'utilisateur ne peut pas changer le user associé
        validated_data.pop("user", None)
        return super().update(instance, validated_data)


class ContactMessageSerializer(serializers.ModelSerializer):
    portfolio_slug = serializers.SlugField(
        source="portfolio.slug", read_only=True
    )

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "portfolio",
            "portfolio_slug",
            "name",
            "email",
            "subject",
            "message",
            "is_read",
            "created_at",
        ]
        read_only_fields = ("id", "portfolio_slug", "is_read", "created_at")


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = [
            "id",
            "to_email",
            "subject",
            "body_preview",
            "status",
            "error_message",
            "meta",
            "created_at",
        ]
        read_only_fields = fields
