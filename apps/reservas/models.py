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
    nombre=models.CharField(max_length=50, unique=True)
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
    paradas=models.ManyToManyField(Parada,related_name="recorridos",blank=True)


    def __str__(self):
        return f'{self.nombre}, {self.estado}, {self.precio}'



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


class Reserva(models.Model):
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    cantidad_personas=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    recorrido=models.ManyToManyField(
        Recorrido,
        related_name='reservas')

    class Meta:
        ordering=['-fecha_creacion']


    def __str__(self):
        return f"Reserva del {self.fecha_creacion:%d/%m/%Y %H:%M} – {self.cantidad_personas} personas"


class Itinerario(models.Model):
    nombre=models.CharField(max_length=30)
    observaciones=models.TextField()
    recorridos=models.ManyToManyField(Recorrido, related_name='itinerarios')

    class Meta:
        ordering=['nombre']

    def __str__(self):
        return f'itinerario: {self.nombre}'
