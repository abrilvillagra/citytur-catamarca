import os
from pyexpat.errors import messages

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecorridoForm, PuntoTuristaForm
from django.contrib import messages
from .models import Recorrido, PuntoTuristico
from django.urls import reverse
#import logging


# Create your views here.
def detalle_recorrido(request, pk):
    recorrido=get_object_or_404(Recorrido, pk=pk)
    return render(request, 'recorridos/detalle_recorrido.html',{'recorrido':recorrido})

def agregar_recorrido(request):
    nuevo_recorrido=None
    if request.method=='POST':
        recorrido_form=RecorridoForm(request.POST, request.FILES)
        if recorrido_form.is_valid():
            nuevo_recorrido=recorrido_form.save(commit=False)
            nuevo_recorrido.save()
            recorrido_form.save_m2m()
            messages.success(request, "Recorrido guardado correctamente.")
            return redirect(reverse('reservas:detalle_recorrido', args=[nuevo_recorrido.id]) )
        else:
            messages.error(request,"Corrige los errores del formulario.")
    else:
        recorrido_form=RecorridoForm()

    return render(request, 'recorridos/gestion_recorridos.html', {'form':recorrido_form})

def editar_recorrido(request, pk):
    recorrido=get_object_or_404(Recorrido, pk=pk)

    if  request.method == 'POST':
        form_recorrido=RecorridoForm(request.POST, request.FILES, instance=recorrido)
        if form_recorrido.is_valid():
            form_recorrido.save()
            messages.success(request, 'Se ha actualizado correctamente el Recorrido')
            return redirect('reservas:detalle_recorrido', pk=recorrido.pk)
    else:
        form_recorrido=RecorridoForm(instance=recorrido)

    return render(request, 'recorridos/gestion_recorridos.html',{'form':form_recorrido} )


def eliminar_recorrido(request, pk):
    recorrido=get_object_or_404(Recorrido, pk=pk)

    if request.method=='POST':
        imagen_path=recorrido.imagen.path if recorrido.imagen else None

        titulo_recorrido=recorrido.nombre
        recorrido.delete()

        if imagen_path and os.path.isfile(imagen_path):
            os.remove(imagen_path)

    return redirect(reverse('reservas:agregar_recorrido'))

def agregar_punto(request):
    nuevo_punto=None
    if request.method=='POST':
        punto_form=PuntoTuristaForm(request.POST, request.FILE)
        if punto_form.is_valid():
            nuevo_punto = punto_form.save(commit=False)
            nuevo_punto.save()
            messages.success(request, "Punto turistico guardado correctamente.")

        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        punto_form=PuntoTuristaForm()

    return render(request, 'recorridos/puntos_turisticos.html', {'form':punto_form})