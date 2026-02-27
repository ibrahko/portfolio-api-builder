from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Theme
from .serializers import ThemeSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Lecture pour tout le monde, écriture réservée aux admins.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ThemeViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur les thèmes.

    - GET /api/themes/           → liste des thèmes actifs (public)
    - GET /api/themes/{id}/      → détail d'un thème
    - POST /api/themes/          → créer un thème (admin)
    - PUT/PATCH /api/themes/{id}/→ modifier un thème (admin)
    - DELETE /api/themes/{id}/   → supprimer un thème (admin)
    """
    queryset = Theme.objects.all().order_by("name")
    serializer_class = ThemeSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        """
        - Public : ne voit que les thèmes actifs.
        - Staff : voit tous les thèmes.
        """
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)

    @action(detail=False, methods=["get"], url_path="featured", permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Optionnel : renvoie un thème "mis en avant".
        Ici on prend simplement le premier thème actif.
        """
        theme = self.get_queryset().filter(is_active=True).first()
        if not theme:
            return Response({"detail": "Aucun thème disponible."}, status=404)
        serializer = self.get_serializer(theme)
        return Response(serializer.data)
