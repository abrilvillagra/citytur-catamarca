from pyexpat.errors import messages

from django.shortcuts import render, redirect
from .forms import RecorridoForm
from django.contrib import messages
import logging


# Create your views here.

def agregar_recorrido(request):

    if request.method=='POST':
        recorrido_form=RecorridoForm(request.POST)
        if recorrido_form.is_valid():
            recorrido_form.save()
            messages.success(request, "Recorrido guardado correctamente.")
            return redirect('reservas:agregar_recorrido')
        else:
            messages.error(request,"Corrige los errores del formulario.")
    else:
        recorrido_form=RecorridoForm()

    return render(request, 'reservas/gestion_recorridos.html', {'form':recorrido_form})
