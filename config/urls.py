from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.themes.views import ThemeViewSet
from apps.portfolios.views import (
    PortfolioViewSet,
    ProjectViewSet,
    SkillViewSet,
    ExperienceViewSet,
    EducationViewSet,
)
from apps.sections.views import SectionViewSet

router = DefaultRouter()
router.register(r"themes", ThemeViewSet, basename="theme")
router.register(r"portfolios", PortfolioViewSet, basename="portfolio")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"educations", EducationViewSet, basename="education")
router.register(r"sections", SectionViewSet, basename="section")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
