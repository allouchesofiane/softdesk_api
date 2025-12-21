from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import date

class User(AbstractUser):
    """
    Modele utilisateur personalisé
    """

    date_of_birth = models.DateField(verbose_name="Date de naissance")
    can_be_contacted = models.BooleanField(default= False, verbose_name="Acceptez-vous d'etre contacté")
    can_data_be_shared = models.BooleanField(default = False, verbose_name="acceptez-vous de partegaer vos données")
    created_time = models.DateTimeField(auto_now_add= True, verbose_name="date de création")

    class Meta:
        verbose_name = "Utilisateur"
        ordering = ['-created_time']

    def __str__(self):
        return self.username
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def clean(self):
        if not self.date_of_birth:
            return

        if self.age < 15:
            raise ValidationError(
                {"date_of_birth": "Vous devez avoir au moins 15 ans pour vous inscrire."}
            )