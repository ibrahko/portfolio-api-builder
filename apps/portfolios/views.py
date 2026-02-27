from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from shared.permissions import IsOwnerOrReadOnly, IsOwnerViaPortfolio
from .models import Portfolio
from .models_project import Project, Skill, Experience, Education, SkillCategory
from .serializers import (
    PortfolioListSerializer,
    PortfolioDetailSerializer,
    PortfolioWriteSerializer,
    ProjectSerializer,
    SkillCategorySerializer,
    SkillSerializer,
    ExperienceSerializer,
    EducationSerializer,
)


class PortfolioViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Portfolio.objects.select_related("theme", "owner").all()
        if self.action in ["list", "retrieve"]:
            return qs.filter(visibility="public")
        if self.request.user.is_authenticated:
            return qs.filter(owner=self.request.user)
        return qs.none()

    def get_serializer_class(self):
        if self.action == "list":
            return PortfolioListSerializer
        if self.action == "retrieve":
            return PortfolioDetailSerializer
        return PortfolioWriteSerializer

    def perform_create(self, serializer):
        # C'est ici que owner est fixé UNE seule fois
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def publish(self, request, slug=None):
        portfolio = self.get_object()
        portfolio.last_published_at = timezone.now()
        portfolio.save(update_fields=["last_published_at"])
        return Response({"status": "published"})


class BasePortfolioChildViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerViaPortfolio]

    def get_queryset(self):
        return self.queryset.filter(portfolio__owner=self.request.user)

    def perform_create(self, serializer):
        portfolio = serializer.validated_data.get("portfolio")
        if portfolio is None:
            raise PermissionDenied("Le champ 'portfolio' est obligatoire.")
        if portfolio.owner != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas ajouter de projet à ce portfolio.")
        serializer.save()


class ProjectViewSet(BasePortfolioChildViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SkillViewSet(BasePortfolioChildViewSet):
    queryset = Skill.objects.select_related("category", "portfolio")
    serializer_class = SkillSerializer


class ExperienceViewSet(BasePortfolioChildViewSet):
    queryset = Experience.objects.select_related("portfolio")
    serializer_class = ExperienceSerializer


class EducationViewSet(BasePortfolioChildViewSet):
    queryset = Education.objects.select_related("portfolio")
    serializer_class = EducationSerializer


class SkillCategoryViewSet(viewsets.ModelViewSet):
    queryset = SkillCategory.objects.all().order_by("sort_order", "name")
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAuthenticated]