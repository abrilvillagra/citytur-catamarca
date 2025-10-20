from django.shortcuts import render, redirect
from .forms import RecorridoForm
# Create your views here.

def agregar_recorrido(request):
    if request.method=='POST':
        recorrido_form=RecorridoForm(request.POST)
        if recorrido_form.is_valid():
            recorrido_form.save()
            return redirect('reservas:gestionar_recorridos')
    else:
        recorrido_form=RecorridoForm()

    return render(request, 'reservas/gestion_recorridos.html', {'recorrido_form':recorrido_form})
