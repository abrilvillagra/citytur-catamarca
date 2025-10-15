from django.db import models
from django.db.models import CharField


# Create your models here.
class Notificacion(models.Model):
    mensaje=models.CharField(max_length=100)
    mail_destinatario=models.EmailField(max_length=254, unique=True)