from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.themes.views import ThemeViewSet
from apps.portfolios.views import (
    PortfolioViewSet,
    ProjectViewSet,
    SkillCategoryViewSet,
    SkillViewSet,
    ExperienceViewSet,
    EducationViewSet,
)
from apps.sections.views import SectionViewSet
from apps.media.views import MediaFileViewSet
from apps.notifications.views import (
    NotificationPreferenceViewSet,
    ContactMessageViewSet,
    EmailLogViewSet,
)

router = DefaultRouter()
# Themes / portfolio / sections
router.register(r"themes", ThemeViewSet, basename="theme")
router.register(r"portfolios", PortfolioViewSet, basename="portfolio")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"skill-categories", SkillCategoryViewSet, basename="skill-category")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"educations", EducationViewSet, basename="education")
router.register(r"sections", SectionViewSet, basename="section")

# Médias
router.register(r"media-files", MediaFileViewSet, basename="media-file")

# Notifications
router.register(
    r"notification-preferences",
    NotificationPreferenceViewSet,
    basename="notification-preference",
)
router.register(
    r"contact-messages",
    ContactMessageViewSet,
    basename="contact-message",
)
router.register(
    r"email-logs",
    EmailLogViewSet,
    basename="email-log",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
