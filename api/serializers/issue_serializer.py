from rest_framework import serializers
from api.models import Issue, Contributor


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "tag",
            "project",
            "author",
            "assigned_to",
            "created_time",
        ]
        read_only_fields = ["id", "author", "created_time"]

    def validate(self, attrs):
        """
        Assigned_to doit être contributeur du projet.
        """
        # project : peut venir de attrs (POST) ou de l'instance (PATCH)
        project = attrs.get("project") or getattr(self.instance, "project", None)
        assigned_to = attrs.get("assigned_to")

        # Si on n'assigne personne, pas de contrainte
        if not assigned_to:
            return attrs

        # Si pas de projet détecté, on laisse DRF gérer l'erreur standard
        if not project:
            return attrs

        is_contributor = Contributor.objects.filter(
            project=project,
            user=assigned_to
        ).exists()

        if not is_contributor:
            raise serializers.ValidationError(
                {"assigned_to": "L'utilisateur assigné doit être contributeur du projet."}
            )

        return attrs