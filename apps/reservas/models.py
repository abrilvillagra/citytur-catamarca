from django.db import models


# Create your models here.

class Reserva(models.Model):
    recorrido=models.ForeignKey('recorridos.Recorrido', on_delete=models.CASCADE, related_name='reservas')

