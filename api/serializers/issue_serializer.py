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
        Règle métier : assigned_to doit être contributeur du projet
        """
        # Récupérer le projet (création ou modification)
        project = attrs.get("project")
        if not project and self.instance:
            project = self.instance.project

        assigned_to = attrs.get("assigned_to")

        # Si pas d'assignation, pas de validation nécessaire
        if not assigned_to:
            return attrs

        # Si pas de projet, on ne peut pas valider (sera géré par DRF)
        if not project:
            return attrs

        # Vérifier que assigned_to est contributeur du projet
        is_contributor = Contributor.objects.filter(
            project=project,
            user=assigned_to
        ).exists()

        if not is_contributor:
            raise serializers.ValidationError(
                {"assigned_to": "L'utilisateur assigné doit être contributeur du projet."}
            )

        return attrs