from pyexpat.errors import messages

from django.shortcuts import render, redirect
from .forms import RecorridoForm
from django.contrib import messages
import logging


# Create your views here.

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
