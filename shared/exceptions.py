import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Handler d'exception centralisé.
    Retourne toujours une réponse JSON structurée.
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "status_code": response.status_code,
            "errors": response.data,
        }
        response.data = error_data
        return response

    # Erreurs non gérées par DRF (ex: IntegrityError, etc.)
    logger.exception(
        "Unhandled exception in view %s",
        context.get("view").__class__.__name__,
        exc_info=exc,
    )
    return Response(
        {
            "status_code": 500,
            "errors": {"detail": "Une erreur interne est survenue."},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
