from django.conf import settings
from django.db import models
from apps.portfolios.models import Portfolio


class NotificationPreference(models.Model):
    """
    Préférences de notification pour un utilisateur.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_prefs",
    )
    receive_contact_emails = models.BooleanField(
        default=True,
        help_text="Recevoir un email quand quelqu'un envoie un message via le portfolio.",
    )
    receive_product_updates = models.BooleanField(
        default=True,
        help_text="Recevoir les nouveautés du Portfolio Builder.",
    )

    def __str__(self) -> str:
        return f"Préférences de {self.user.username}"


class ContactMessage(models.Model):
    """
    Message envoyé via le formulaire de contact public d'un portfolio.
    """
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="contact_messages",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message de {self.name} pour {self.portfolio}"


class EmailLog(models.Model):
    """
    Log technique des emails envoyés (pour debug / monitoring).
    """
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body_preview = models.CharField(
        max_length=255,
        help_text="Les premiers caractères du message pour référence.",
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ("sent", "Envoyé"),
            ("failed", "Échec"),
        ),
    )
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.status.upper()} — {self.subject} → {self.to_email}"
