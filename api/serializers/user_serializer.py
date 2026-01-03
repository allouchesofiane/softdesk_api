from rest_framework import serializers
from api.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import date

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        # Ce que l'API accepte
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
            'date_of_birth',
            'can_be_contacted',
            'can_data_be_shared',
        ]
        read_only_fields = ['id']

    def validate_date_of_birth(self, value):
        """
        Vérifier que l'utilisateur a au moins 15 ans
        """
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )
    
        if age < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour vous inscrire."
            )
    
        return value
    
    def validate(self, data):
        """
        Validation globale des données
        """
        # Vérifier que les mots de passe correspondent
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })

        # Valider la force du mot de passe
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data):
        """
        Créer un nouvel utilisateur avec validation RGPD
        """
        # Retirer password_confirm avant de créer l'utilisateur
        validated_data.pop('password_confirm')

        # Créer l'utilisateur avec mot de passe haché
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False),
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher les informations d'un utilisateur
    """
    age = serializers.ReadOnlyField()

    class Meta:
        model = User
        # Ce que l'API renvoie
        fields = [
            'id',
            'username',
            'email',
            'date_of_birth',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'created_time',
        ]
        # ne peuvent pas être modifiés, sont ignorés si envoyés par le client
        read_only_fields = ['id', 'created_time', 'age']