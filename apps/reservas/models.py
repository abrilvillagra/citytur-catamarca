from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class FormaPago(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.CharField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre}'

class Reserva(models.Model):
    forma_pago=models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    fechaCreacion=models.DateField(auto_now_add=True)
    cant_personas=models.IntegerField(validators=[MinValueValidator(1)])
    recorrido=models.ForeignKey('recorridos.Recorrido', on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='reservas')
    estado=models.BooleanField(default=True)

    def __str__(self):
        return f'reserva: {self.recorrido}, {self.estado}'

