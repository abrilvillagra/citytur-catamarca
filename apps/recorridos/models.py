from django.db import models

# Create your models here.

class Recorrido(models.Model):
    nombre=models.CharField(max_length=100)
    horaInicio=models.TimeField(auto_now_add=True)
    horaFin=models.TimeField(auto_now_add=True)
    precio=models.FloatField()
    estado=models.BooleanField(default=True)
    fecha=models.DateField(auto_now_add=True)
    paradas=models.ManyToManyField('paradas.Parada')

    def __str__(self):
        return f'{self.nombre}, {self.estado}, {self.precio}'