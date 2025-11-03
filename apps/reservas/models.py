from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class PuntoTuristico(models.Model):
    CATEGORIA=[
        ('NATURAL','Natural'),
        ('CULTURAL', 'Cultural'),
        ('GASTRONOMIA','Gastronimia'),
        ('RELIGIOSO', 'Religiosa'),
    ]

    nombre=models.CharField(max_length=50)
    categoria=models.CharField(max_length=20, choices=CATEGORIA, default='CULTURAL')
    descripcion=models.TextField(blank=True)
    ubicacion=models.CharField(max_length=100)
    estado=models.BooleanField(default=True)

    class Meta:
        ordering=['nombre']
        verbose_name = "Punto turístico"
        verbose_name_plural = "Puntos turísticos"

    def __str__(self):
        return f'{self.nombre}, {self.estado}'


class Recorrido(models.Model):
    nombre=models.CharField(max_length=50, unique=True)
    descripcion=models.TextField(blank=True)
    hora_salida=models.TimeField()
    hora_llegada=models.TimeField()
    estado=models.BooleanField(default=True)
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    imagen=models.FileField(blank=True,  null=True)
    precio=models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    puntos_turisticos=models.ManyToManyField(PuntoTuristico,related_name="recorridos",blank=True)


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
    FORMA_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRASNFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
        ('QR', 'Codigo QR'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    forma_de_pago = models.CharField(max_length=20, choices=FORMA_PAGO, default="EFECTIVO")
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    fecha_reserva = models.DateField()
    cantidad_personas=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    recorrido=models.ForeignKey(
        Recorrido,
        on_delete=models.CASCADE,
        related_name='reservas')

    class Meta:
        ordering=['-fecha_creacion']


    def __str__(self):
        return f"Reserva {self.nombre_completo} – {self.recorrido} – {self.fecha_reserva:%d/%m/%Y} – {self.cantidad_personas} pax"



