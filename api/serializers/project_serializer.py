from rest_framework import serializers
from api.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour les projets
    """
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'created_time',
        ]
        read_only_fields = ['id', 'author', 'created_time']