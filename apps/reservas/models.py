from django.db import models


# Create your models here.

class Reserva(models.Model):
    FORMA_PAGO = [
        ('EF', 'Efectivo'),
        ('TJ', 'Tarjeta'),
        ('TR', 'Transferencia'),
    ]
    recorrido=models.ForeignKey('recorridos.Recorrido', on_delete=models.CASCADE, related_name='reservas')
    cantidad_personas=models.IntegerField()
    fecha_creacion=models.DateField()
