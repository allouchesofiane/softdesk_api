from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import date

class User(AbstractUser):
    """
    Modele utilisateur personalisé
    """

    date_of_birth = models.DateField(
        verbose_name="Date de naissance"
    )
    
    can_be_contacted = models.BooleanField(
        default= False, 
        verbose_name="Acceptez-vous d'etre contacté"
    )
    
    can_data_be_shared = models.BooleanField(
        default = False, 
        verbose_name="acceptez-vous de partegaer vos données"
    )
    
    created_time = models.DateTimeField(
        auto_now_add= True, verbose_name="date de création"
    )

    class Meta:
        verbose_name = "Utilisateur"
        ordering = ['-created_time']

    def __str__(self):
        return self.username
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (
            self.date_of_birth.month, self.date_of_birth.day
        ):
            age -= 1
        return age

    def clean(self):
        if not self.date_of_birth:
            return None

        if self.age < 15:
            raise ValidationError(
                {"date de naissance": "Vous devez avoir au moins 15 ans pour vous inscrire."}
            )
        

class Project(models.Model):
    """
    Modèle représentant un projet
    """
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Nom du projet"
    )
    
    description = models.TextField(
        verbose_name="Description"
    )
    
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type de projet"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_projects',
        verbose_name="Auteur"
    )
    
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Projet"
        ordering = ['-created_time']

    def __str__(self):
        return self.name
    

class Contributor(models.Model):
    """
    Modèle représentant un contributeur d'un projet
    """
    ROLE_CHOICES = [
        ('author', 'Auteur'),
        ('contributor', 'Contributeur'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contributions',
        verbose_name="Utilisateur"
    )
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors',
        verbose_name="Projet"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='contributor',
        verbose_name="Rôle"
    )
    
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )

    class Meta:
        verbose_name = "Contributeur"
        ordering = ['-created_time']
        unique_together = ['user', 'project']

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"