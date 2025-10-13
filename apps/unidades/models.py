from django.db import models

# Create your models here.

class Unidad(models.Model):
    numero_unidad=models.IntegerField(unique=True)
    capacidad_maxima=models.IntegerField()

    def __str__(self):
        return f'{self.numero_unidad}, {self.capacidad_maxima}'

