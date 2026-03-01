import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def flush_expired_tokens():
    """
    Supprime les tokens JWT blacklistés expirés.
    Tâche périodique (Celery Beat).
    """
    from rest_framework_simplejwt.token_blacklist.models import (
        OutstandingToken,
        BlacklistedToken,
    )
    from django.utils import timezone

    expired = OutstandingToken.objects.filter(expires_at__lt=timezone.now())
    count = expired.count()
    BlacklistedToken.objects.filter(token__in=expired).delete()
    expired.delete()
    logger.info("%d token(s) JWT expirés supprimés.", count)
    return count
