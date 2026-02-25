from django.conf import settings
from django.db import models


class MediaFile(models.Model):
    """
    Fichier média générique (image, PDF, etc.) lié à un utilisateur.
    Réutilisable dans plusieurs portfolios / projets.
    """
    FILE_TYPES = (
        ("image", "Image"),
        ("document", "Document"),
        ("video", "Vidéo"),
        ("other", "Autre"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="media_files",
    )
    file = models.FileField(upload_to="media_files/%Y/%m/")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default="image")
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    size_bytes = models.PositiveBigIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.file.name

    def save(self, *args, **kwargs):
        if self.file and not self.size_bytes:
            self.size_bytes = self.file.size
        super().save(*args, **kwargs)
