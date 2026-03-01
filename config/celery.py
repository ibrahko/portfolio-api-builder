import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("neka_portfolio")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "flush-expired-tokens": {
        "task": "apps.accounts.tasks.flush_expired_tokens",
        "schedule": crontab(hour=2, minute=0),
    },
    "clean-old-email-logs": {
        "task": "apps.notifications.tasks.clean_old_email_logs",
        "schedule": crontab(hour=3, minute=0, day_of_week=1),
    },
}
