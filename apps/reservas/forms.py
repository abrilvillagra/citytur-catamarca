from django import forms
from django.forms.widgets import TextInput

from .models import Recorrido, Parada
from django import forms

from apps.reservas.models import Recorrido

class RecorridoForm(forms.ModelForm):
    paradas=forms.ModelMultipleChoiceField(
        queryset=Parada.objects.filter(estado=True),
        widget=forms.SelectMultiple(attrs={
            'class':'form-select',
            'id':'paradas'
        }),
        required=False
    )

    class Meta:
        model=Recorrido
        fields=['nombre', 'precio', 'hora_salida', 'hora_llegada', 'estado', 'descripcion', 'paradas']
        widgets={
            'nombre': forms.TextInput(attrs={'required':'True'}),
            'precio': forms.NumberInput(attrs={'min':'1', 'required':'True'}),
            'hora_salida': forms.TimeInput(attrs={})

        }
