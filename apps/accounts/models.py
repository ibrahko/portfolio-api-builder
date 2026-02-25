from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    Profil étendu pour l'utilisateur (Django User).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    headline = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ex: Développeur Fullstack | Django & React",
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self) -> str:
        return self.full_name or self.user.username
