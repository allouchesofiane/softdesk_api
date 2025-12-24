from rest_framework import serializers
from api.models import Issue


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
