from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Contributor


class IsProjectAuthorForContributor(BasePermission):
    """
    Lecture: autorisée aux contributeurs du projet
    Écriture: réservée à l'auteur du projet
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return Contributor.objects.filter(
                user=request.user,
                project=obj.project
            ).exists()
        return obj.project.author == request.user
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            project_id = request.data.get("project")
            if not project_id:
                return False
            return Contributor.objects.filter(
                user=request.user,
                project_id=project_id,
                role="author"
            ).exists()

        return True
