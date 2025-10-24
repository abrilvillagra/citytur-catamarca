from pyexpat.errors import messages

from django.shortcuts import render, redirect
from .forms import RecorridoForm
from django.contrib import messages
from apps.reservas.forms import ReservaForm
from apps.reservas.models import Reserva

import logging


# Create your views here.

def inicio(request):
    return render(request, 'reservas/inicio.html')
def agregar_recorrido(request):
    nuevo_recorrido=None
    if request.method=='POST':
        recorrido_form=RecorridoForm(request.POST, request.FILES)
        if recorrido_form.is_valid():
            nuevo_recorrido=recorrido_form.save(commit=False)
            nuevo_recorrido.save()
            recorrido_form.save_m2m()
            messages.success(request, "Recorrido guardado correctamente.")
            return redirect('reservas:agregar_recorrido')
        else:
            messages.error(request,"Corrige los errores del formulario.")
    else:
        recorrido_form=RecorridoForm()

    return render(request, 'reservas/gestion_recorridos.html', {'form':recorrido_form})

def crear_reserva(request):
    """
    Vista para crear una nueva reserva.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu reserva fue registrada correctamente!")
            return redirect('reservas_crear')
        else:
            messages.error(request, "Por favor corregí los errores antes de enviar.")
    else:
        form = ReservaForm()

    return render(request, 'reservas/form_reserva.html', {'form': form})

