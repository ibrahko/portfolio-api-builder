from django.db import models
from apps.portfolios.models import Portfolio


class Section(models.Model):
    SECTION_TYPES = (
        ("hero", "Hero"),
        ("about", "À propos"),
        ("projects", "Projets"),
        ("skills", "Compétences"),
        ("experience", "Expériences"),
        ("education", "Éducation"),
        ("contact", "Contact"),
        ("custom", "Personnalisée"),
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    type = models.CharField(max_length=30, choices=SECTION_TYPES)
    title = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(
        max_length=80,
        help_text="Identifiant unique dans le portfolio (ancre de section).",
    )
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    # Config supplémentaire légère (pas le contenu métier)
    settings = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("portfolio", "slug")

    def __str__(self) -> str:
        return f"{self.portfolio.title} — {self.get_type_display()}"
