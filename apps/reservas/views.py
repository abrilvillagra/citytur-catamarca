from pyexpat.errors import messages

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecorridoForm
from django.contrib import messages
from .models import Recorrido
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
