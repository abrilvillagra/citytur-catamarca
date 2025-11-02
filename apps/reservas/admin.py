from django.contrib import admin
from .models import PuntoTuristico, Recorrido, Reserva

# Register your models here.

@admin.register(PuntoTuristico)
class PuntoTuristicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'descripcion' ,'ubicacion', 'estado')

@admin.register(Recorrido)
class RecorridoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_salida', 'estado', 'precio')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'telefono', 'fecha_creacion', 'recorrido')