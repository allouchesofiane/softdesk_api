from rest_framework import serializers
from api.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "description",
            "issue",
            "author",
            "created_time",
        ]
        read_only_fields = ["id", "uuid", "author", "created_time"]
