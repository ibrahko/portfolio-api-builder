from rest_framework import viewsets, permissions, mixins
from rest_framework.exceptions import PermissionDenied

from .models import NotificationPreference, ContactMessage, EmailLog
from .serializers import (
    NotificationPreferenceSerializer,
    ContactMessageSerializer,
    EmailLogSerializer,
)
from shared.permissions import IsOwnerViaPortfolio

class NotificationPreferenceViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Empêche de créer des prefs pour un autre user
        serializer.save(user=self.request.user)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    - POST (AllowAny) : créer un message de contact pour un portfolio public.
    - GET/PUT/PATCH (IsAuthenticated) : le propriétaire du portfolio lit/marque comme lu.
    """
    queryset = ContactMessage.objects.select_related("portfolio", "portfolio__owner")
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Pour lecture/modif, limiter aux messages des portfolios de l'utilisateur
        if self.request.user.is_authenticated:
            return (
                ContactMessage.objects.select_related("portfolio", "portfolio__owner")
                .filter(portfolio__owner=self.request.user)
                .order_by("-created_at")
            )
        # Pour POST, on n'utilise pas le queryset
        return ContactMessage.objects.none()

    def perform_create(self, serializer):
        """
        Ici tu peux ajouter des validations supplémentaires :
        - vérifier que le portfolio est bien 'public'
        - lancer une tâche Celery pour envoyer un email de notification
        """
        portfolio = serializer.validated_data.get("portfolio")
        if portfolio.visibility != "public":
            raise PermissionDenied("Ce portfolio n'accepte pas de messages publics.")
        serializer.save()


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Logs des emails envoyés (pour debug). Visible uniquement par staff.
    """
    queryset = EmailLog.objects.all().order_by("-created_at")
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAdminUser]

