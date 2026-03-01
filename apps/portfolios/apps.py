from django.apps import AppConfig


class PortfoliosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.portfolios"
    verbose_name = "Portfolios"

    def ready(self):
        import apps.portfolios.signals
