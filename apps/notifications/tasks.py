import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import ContactMessage, EmailLog

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_contact_notification(self, contact_message_id: int):
    """
    Envoie un email au propriétaire du portfolio
    quand il reçoit un nouveau message de contact.
    """
    try:
        message = ContactMessage.objects.select_related(
            "portfolio__owner"
        ).get(id=contact_message_id)

        owner = message.portfolio.owner
        subject = f"[Neka] Nouveau message de {message.name}"
        body = (
            f"Bonjour {owner.username},\n\n"
            f"Vous avez reçu un message de {message.name} "
            f"({message.email}) :\n\n"
            f"Sujet : {message.subject}\n\n"
            f"{message.message}\n\n"
            f"— L'équipe Neka"
        )

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner.email],
            fail_silently=False,
        )

        EmailLog.objects.create(
            to_email=owner.email,
            subject=subject,
            body_preview=body[:255],
            status="sent",
        )

        logger.info(
            "Email de contact envoyé à %s pour le portfolio '%s'.",
            owner.email,
            message.portfolio.title,
        )

    except ContactMessage.DoesNotExist:
        logger.error("ContactMessage ID %s introuvable.", contact_message_id)

    except Exception as exc:
        EmailLog.objects.create(
            to_email="unknown",
            subject="Erreur envoi contact",
            body_preview=str(exc)[:255],
            status="failed",
            error_message=str(exc),
        )
        logger.exception(
            "Erreur lors de l'envoi du mail de contact ID %s.",
            contact_message_id,
        )
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_id: int):
    """
    Envoie un email de bienvenue à un nouvel utilisateur.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        subject = "Bienvenue sur Neka Portfolio !"
        body = (
            f"Bonjour {user.username},\n\n"
            f"Votre compte a bien été créé sur Neka Portfolio.\n"
            f"Vous pouvez dès maintenant créer votre premier portfolio.\n\n"
            f"— L'équipe Neka"
        )

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        EmailLog.objects.create(
            to_email=user.email,
            subject=subject,
            body_preview=body[:255],
            status="sent",
        )

        logger.info("Email de bienvenue envoyé à %s.", user.email)

    except User.DoesNotExist:
        logger.error("User ID %s introuvable pour welcome email.", user_id)

    except Exception as exc:
        logger.exception(
            "Erreur lors de l'envoi du welcome email à user ID %s.", user_id
        )
        raise self.retry(exc=exc)


@shared_task
def clean_old_email_logs():
    """
    Supprime les EmailLog de plus de 90 jours.
    Tâche périodique (Celery Beat).
    """
    cutoff = timezone.now() - timedelta(days=90)
    deleted_count, _ = EmailLog.objects.filter(created_at__lt=cutoff).delete()
    logger.info("%d EmailLog(s) supprimé(s) (> 90 jours).", deleted_count)
    return deleted_count
