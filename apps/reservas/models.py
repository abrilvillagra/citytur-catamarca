from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Parada(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)

    class Meta:
        ordering=['nombre']

    def __str__(self):
        return f'{self.nombre}, {self.estado}'


class Recorrido(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()
    hora_salida=models.TimeField()
    hora_llegada=models.TimeField()
    estado=models.BooleanField(default=True)
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    precio=models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    paradas=models.ManyToManyField(
        Parada,
        through='RecorridoParada',
        related_name='recorridos'

    )


    def __str__(self):
        return f'{self.nombre}, {self.estado}, {self.precio}'


#defino nuestra propia tabla intermedia entre Recorrido y Parada para poder agregar campos
#como orden y tiempo de espera
class RecorridoParada(models.Model):
    recorrido=models.ForeignKey(Recorrido,on_delete=models.CASCADE)
    parada=models.ForeignKey(Parada, on_delete=models.CASCADE)
    orden=models.PositiveIntegerField()
    tiempo_espera_minutos=models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('recorrido', 'orden')
        ordering=['recorrido', 'orden']

class UnidadTransporte(models.Model):
    patente=models.CharField(max_length=7, unique=True)
    marca=models.CharField(max_length=50)
    modelo=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)

    recorrido=models.ForeignKey(
        Recorrido,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unidades'
    )

    class Meta:
        ordering=['patente']

    def __str__(self):
        return  f'{self.patente}, {self.marca}, {self.estado}'





