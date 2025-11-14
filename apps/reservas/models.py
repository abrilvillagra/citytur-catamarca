from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models,transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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


class UnidadTransporte(models.Model):
    patente=models.CharField(max_length=7, unique=True)
    marca=models.CharField(max_length=50)
    modelo=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)
    capacidad=models.PositiveIntegerField(default=20)

    class Meta:
        ordering=['patente']

    def __str__(self):
        return  f'{self.patente}, {self.marca}, {self.estado}'



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

    unidad = models.OneToOneField(
        UnidadTransporte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorridos"
    )

    def __str__(self):
        return f'{self.nombre}, {self.estado}, {self.precio}'

    @property
    def capacidad(self):
        """Capacidad del recorrido = capacidad de la unidad asignada (o 0 si no hay unidad)."""
        return self.unidad.capacidad if self.unidad else 0

    def save(self, *args, **kwargs):

        # unidad anterior (si existe)
        unidad_anterior = None
        if self.pk:
            try:
                unidad_anterior = Recorrido.objects.get(pk=self.pk).unidad
            except Recorrido.DoesNotExist:
                unidad_anterior = None

        nueva_unidad = self.unidad

        if nueva_unidad and not nueva_unidad.estado:
            # la unidad está ocupada/inactiva: impedir asignación
            raise ValidationError("No se puede asignar una unidad inactiva u ocupada.")

        with transaction.atomic():
            super().save(*args, **kwargs)  # guardamos recorrido (necesario para algunos casos)

            # si cambiamos de unidad: reactivar la anterior y desactivar la nueva
            if unidad_anterior and unidad_anterior != nueva_unidad:
                unidad_anterior.estado = True
                unidad_anterior.save(update_fields=['estado'])

            if nueva_unidad and unidad_anterior != nueva_unidad:
                nueva_unidad.estado = False
                nueva_unidad.save(update_fields=['estado'])

    def delete(self, *args, **kwargs):
        """
        Reactiva la unidad asociada al eliminar el recorrido.
        (Nota: para borrados en masa también registramos signal post_delete más abajo)
        """
        unidad = self.unidad
        super().delete(*args, **kwargs)
        if unidad:
            unidad.estado = True
            unidad.save(update_fields=['estado'])

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



