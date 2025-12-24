from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Contributor


class IsProjectContributor(BasePermission):
    """
    Autorise l'accès uniquement aux contributeurs du projet.
    (SAFE_METHODS inclus : lecture)
    """

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(user=request.user, project=obj).exists()


class IsProjectAuthor(BasePermission):
    """
    Autorise modification/suppression uniquement à l'auteur du projet.
    La lecture reste gérée par IsProjectContributor.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
