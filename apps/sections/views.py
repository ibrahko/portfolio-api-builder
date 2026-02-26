from rest_framework import viewsets
from shared.permissions import IsOwnerViaPortfolio
from .models import Section
from .serializers import SectionSerializer


class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerViaPortfolio]
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(
            portfolio__owner=self.request.user
        ).select_related("portfolio")
