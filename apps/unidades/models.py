from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Unidad(models.Model):
    patente=models.CharField(max_length=100)
    capacidad=models.IntegerField(validators=[MinValueValidator(1)])
    marca=models.CharField(max_length=40)
    modelo=models.CharField(max_length=40)
    estado=models.BooleanField(default=True)
