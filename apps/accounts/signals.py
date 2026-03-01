import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile
from apps.notifications.models import NotificationPreference

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile_and_preferences(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        NotificationPreference.objects.get_or_create(user=instance)
        logger.info(
            "Profil et préférences créés pour : %s",
            instance.username,
        )
