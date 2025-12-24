from rest_framework import serializers
from api.models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "role",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]
