import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Portfolio

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Portfolio)
def log_portfolio_saved(sender, instance, created, **kwargs):
    action = "créé" if created else "mis à jour"
    logger.info(
        "Portfolio '%s' (owner: %s) %s.",
        instance.title,
        instance.owner.username,
        action,
    )


@receiver(post_delete, sender=Portfolio)
def log_portfolio_deleted(sender, instance, **kwargs):
    logger.warning(
        "Portfolio '%s' (owner: %s) supprimé.",
        instance.title,
        instance.owner.username,
    )
