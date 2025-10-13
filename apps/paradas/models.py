from django.db import models

# Create your models here.

class Parada(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'