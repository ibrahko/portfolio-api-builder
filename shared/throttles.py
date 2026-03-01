from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterThrottle(AnonRateThrottle):
    """Limite le nombre d'inscriptions depuis une même IP."""
    rate = "10/hour"
    scope = "register"


class LoginThrottle(AnonRateThrottle):
    """Limite le nombre de tentatives de login."""
    rate = "20/hour"
    scope = "login"
