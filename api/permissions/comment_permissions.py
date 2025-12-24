from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Contributor


class IsCommentIssueProjectContributor(BasePermission):
    """
    Autorise l'accès uniquement aux contributeurs du projet lié à l'issue du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            user=request.user,
            project=obj.issue.project
        ).exists()


class IsCommentAuthor(BasePermission):
    """
    Autorise modification/suppression uniquement à l'auteur du commentaire.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
