from django.db import models

# Create your models here.

class Recorrido(models.Model):
    nombre=models.CharField(max_length=100)
    cupos=models.IntegerField()
    paradas=models.ManyToManyField('paradas.Parada', related_name='recorridos',
                                   blank=True)
    activo=models.BooleanField(default=True)
    fecha_y_hora=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre}, {self.paradas}, {self.cupos}'