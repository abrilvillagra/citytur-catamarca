
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):


    def __str__(self):
        return f"{self.username}"

    def obtener_nombre_completo(self):
        if self.last_name and self.first_name:
            nombre_completo = f"{self.last_name}, {self.first_name}"
            return nombre_completo.strip()
        else:
            return self.username

    obtener_nombre_completo.short_description = "Nombre Completo"



