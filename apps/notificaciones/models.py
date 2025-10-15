from django.db import models


# Create your models here.

class Notificacion(models.Model):
    mensaje=models.CharField(max_length=100)
    mail_destinatario=models.EmailField()
