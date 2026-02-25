from django.conf import settings
from django.db import models
from apps.themes.models import Theme


class Portfolio(models.Model):
    """
    Portfolio d'un utilisateur (peut en avoir plusieurs).
    """
    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("unlisted", "Non listé"),
        ("private", "Privé"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolios",
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=80, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        null=True,
        related_name="portfolios",
    )
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )
    custom_domain = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optionnel: sous-domaine ou domaine custom.",
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Portfolio principal de l'utilisateur.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_published_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Dernière fois où l'utilisateur a cliqué sur 'Publier'.",
    )

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.owner.username})"
