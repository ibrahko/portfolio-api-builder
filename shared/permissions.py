from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Lecture publique si l'objet est 'public' (pour Portfolio),
    écriture réservée au propriétaire.
    Suppose que l'objet a des attributs 'owner' et 'visibility'.
    """

    def has_object_permission(self, request, view, obj):
        # Méthodes de lecture
        if request.method in permissions.SAFE_METHODS:
            visibility = getattr(obj, "visibility", None)
            if visibility == "public":
                return True
            if request.user.is_authenticated and getattr(obj, "owner", None) == request.user:
                return True
            return False

        # Méthodes d'écriture
        return request.user.is_authenticated and getattr(obj, "owner", None) == request.user


class IsOwnerViaPortfolio(permissions.BasePermission):
    """
    Pour les modèles enfants (Project, Skill, Experience, Education, Section).
    On vérifie que obj.portfolio.owner == request.user.
    """

    def has_object_permission(self, request, view, obj):
        portfolio = getattr(obj, "portfolio", None)
        if portfolio is None:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and portfolio.owner == request.user

        return request.user.is_authenticated and portfolio.owner == request.user
