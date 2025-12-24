from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers.user_serializer import UserRegistrationSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from api.serializers.project_serializer import ProjectSerializer
from api.permissions.project_permissions import IsProjectContributor, IsProjectAuthor
from api.models import Project, Contributor


@api_view(['POST'])
@permission_classes([AllowAny]) 
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

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectContributor & IsProjectAuthor]

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