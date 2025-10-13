from django.db import models
from ..recorridos.models import Recorrido
from ..usuarios.models import Usuario
# Create your models here.

class Reserva(models.Model):
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    recorrido=models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='reservas')

