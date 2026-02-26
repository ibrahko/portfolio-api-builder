from rest_framework import viewsets, permissions
from .models import Theme
from .serializers import ThemeSerializer


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des thèmes disponibles (lecture seule côté public).
    """
    queryset = Theme.objects.filter(is_active=True).order_by("name")
    serializer_class = ThemeSerializer
    permission_classes = [permissions.AllowAny]
