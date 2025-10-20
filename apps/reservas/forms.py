from django import forms
from .models import Recorrido, Parada

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

