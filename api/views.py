from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.serializers.user_serializer import UserRegistrationSerializer, UserSerializer


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
