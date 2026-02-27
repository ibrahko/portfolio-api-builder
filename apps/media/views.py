from rest_framework import viewsets, permissions, parsers
from shared.permissions import IsOwnerOrReadOnly  # ou une permission dédiée si tu en as
from .models import MediaFile
from .serializers import MediaFileSerializer


class MediaFileViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les fichiers média de l'utilisateur connecté.
    Upload via multipart/form-data.
    """
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        # Chaque user ne voit que ses propres fichiers
        return MediaFile.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
