from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator


# Create your models here.

#default='ejemplo@ejemplo.com'

class Usuario(AbstractUser):
    ROLES= (
        ('usuario', 'Usuario'),
        ('admin', 'Administrador')
    )
    rol=models.CharField(max_length=20, choices=ROLES, default='usuario')
    nombre=models.CharField(max_length=100)
    dni=models.CharField(max_length=11, unique=True)
    mail=models.EmailField(max_length=150,null=True,default='ejemplo@ejemplo.com',
                           validators=[EmailValidator(message="ingrese un mail valido")])
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\+?1?\d{9,10}$', message="Formato: +999999999. Hasta 10 dígitos.")],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.nombre}, {self.dni}, {self.rol}'
