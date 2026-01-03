from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Contributor


class IsIssueProjectContributor(BasePermission):
    """
    Autorise l'accès uniquement aux contributeurs du projet lié à l'issue.
    """

    def has_object_permission(self, request, obj):
        return Contributor.objects.filter(user=request.user, project=obj.project).exists()


class IsIssueAuthor(BasePermission):
    """
    Autorise modification/suppression uniquement à l'auteur de l'issue.
    """

    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
