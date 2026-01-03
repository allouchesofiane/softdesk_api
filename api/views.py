from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.user_serializer import UserRegistrationSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from api.serializers.project_serializer import ProjectSerializer
from api.permissions.project_permissions import IsProjectContributor, IsProjectAuthor
from api.models import Project, Contributor, Issue, Comment
from api.serializers.contributor_serializer import ContributorSerializer
from api.serializers.issue_serializer import IssueSerializer
from api.permissions.issue_permissions import IsIssueProjectContributor, IsIssueAuthor
from api.serializers.comment_serializer import CommentSerializer
from api.permissions.comment_permissions import IsCommentIssueProjectContributor, IsCommentAuthor
from api.permissions.contributor_permissions import IsProjectAuthorForContributor


@api_view(['POST']) # Cette URL accepte uniquement POST
@permission_classes([AllowAny]) # Tout le monde peut appeler cette route (même sans être connecté)
def signup(request):
    """
    Endpoint d'inscription d'un nouvel utilisateur
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        
        return Response(
            {
                "message": "Utilisateur créé avec succès",
                "user": user_data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Récupérer les informations de l'utilisateur connecté
    Nécessite une authentification JWT
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Projet
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsProjectAuthor]

    def get_queryset(self):
        return Project.objects.filter(
            contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.get_or_create(
            user=self.request.user,
            project=project,
            defaults={"role": "author"},
        )

# Contributeur
class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorForContributor]

    def get_queryset(self):
        return Contributor.objects.filter(
            project__contributors__user=self.request.user
        ).distinct()
    

# Issue
class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsIssueProjectContributor, IsIssueAuthor]

    def get_queryset(self):
        return Issue.objects.filter(
            project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Comment
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsCommentIssueProjectContributor, IsCommentAuthor
    ]

    def get_queryset(self):
        return Comment.objects.filter(
            issue__project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)