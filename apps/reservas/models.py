from decimal import Decimal
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models,transaction
from django.db.models import Sum
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

        # obtener la unidad anterior (si existe)
        unidad_anterior = None
        if self.pk:
            try:
                unidad_anterior = Recorrido.objects.get(pk=self.pk).unidad
            except Recorrido.DoesNotExist:
                unidad_anterior = None

        nueva_unidad = self.unidad

        # Si la unidad no cambió, simplemente guardamos y salimos
        if unidad_anterior and unidad_anterior == nueva_unidad:
            # No necesitamos cambiar estados: la unidad ya estaba asociada a este recorrido
            super().save(*args, **kwargs)
            return

        # Si la unidad cambió o es nueva, validamos que la nueva unidad esté disponible
        if nueva_unidad:
            # si la nueva unidad está inactiva y no es la unidad anterior -> no se puede asignar
            if not nueva_unidad.estado and unidad_anterior != nueva_unidad:
                raise ValidationError("La unidad seleccionada no está disponible (ya asignada).")

        # Hacemos el cambio en una transacción
        with transaction.atomic():
            # Guardamos el recorrido primero (necesario si es creación)
            super().save(*args, **kwargs)

            # Si había una unidad anterior distinta: reactivarla
            if unidad_anterior and unidad_anterior != nueva_unidad:
                unidad_anterior.estado = True
                unidad_anterior.save(update_fields=['estado'])

            # Si hay una nueva unidad distinta de la anterior: inactivarla
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

    def puede_cancelar(self, hoy=None):

        if hoy is None:
            hoy = timezone.localdate()

        # Si ya está inactiva, no tiene sentido "cancelar" otra vez
        if not self.activa:
            return False, "La reserva ya está cancelada."

        # Diferencia en días entre fecha_reserva y hoy
        dias = (self.fecha_reserva - hoy).days

        if dias <= 1:
            # Mensaje claro para el usuario
            return False, (
                "No es posible cancelar la reserva con 1 día de anticipación (o menos). "
                "Por ejemplo, una reserva para el 12/12/2025 no puede ser cancelada el 11/12/2025."
            )

        return True, None

    def clean(self):
        super().clean()

        if not self.recorrido or not self.fecha_reserva:
            return

        # Capacidad del recorrido
        capacidad = self.recorrido.capacidad

        # Total ya reservado (solo reservas activas)
        qs = Reserva.objects.filter(
            recorrido=self.recorrido,
            fecha_reserva=self.fecha_reserva,
            activa=True
        )

        # Si estoy modificando una reserva, no me cuento a mí mismo
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        reservado = qs.aggregate(total=Sum('cantidad_personas'))['total'] or 0

        # Cantidad que quiere reservar el usuario
        cantidad = self.cantidad_personas

        if reservado + cantidad > capacidad:
            disponibles = capacidad - reservado
            raise ValidationError({
                'cantidad_personas': f"No hay suficientes cupos. Quedan {disponibles} disponibles."
            })


