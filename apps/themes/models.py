from django.db import models


class Theme(models.Model):
    """
    Thème visuel d'un portfolio (template).
    """
    SLUG_MAX_LENGTH = 50

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    description = models.TextField(blank=True)

    # Config visuelle simple (tu pourras enrichir plus tard)
    primary_color = models.CharField(
        max_length=7,
        default="#4F46E5",
        help_text="Couleur principale (hex).",
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#111827",
        help_text="Couleur secondaire (hex).",
    )
    background_color = models.CharField(
        max_length=7,
        default="#F9FAFB",
    )
    text_color = models.CharField(
        max_length=7,
        default="#111827",
    )
    font_family = models.CharField(
        max_length=100,
        default="Inter, system-ui, -apple-system, BlinkMacSystemFont",
    )

    preview_image = models.ImageField(
        upload_to="themes/previews/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"

    def __str__(self) -> str:
        return self.name
