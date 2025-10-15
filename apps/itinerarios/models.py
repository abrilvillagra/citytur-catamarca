from django.db import models

# Create your models here.

class Itinerario(models.Model):
    nombre=models.CharField(max_length=100)
    observaciones=models.TextField(blank=True)
    recorridos=models.ManyToManyField('recorridos.Recorrido')

    def __str__(self):
        return f'{self.nombre}'