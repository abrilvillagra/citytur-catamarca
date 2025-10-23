
from django import forms

from apps.reservas.models import Recorrido, PuntoTuristico

class RecorridoForm(forms.ModelForm):
    paradas=forms.ModelMultipleChoiceField(
        queryset=PuntoTuristico.objects.filter(estado=True),
        widget=forms.SelectMultiple(attrs={
            'class':'form-select',
            'id':'paradas',
            'size': 5
        }),
        required=False
    )

    class Meta:
        model=Recorrido
        fields=['nombre', 'precio', 'hora_salida', 'hora_llegada', 'estado', 'descripcion', 'paradas']
        ESTADOS = [
            (True, 'Activo'),
            (False, 'Inactivo'),
        ]
        widgets={
            'nombre': forms.TextInput(attrs={'required':'True'}),
            'precio': forms.NumberInput(attrs={'min':'1', 'required':'True'}),
            'hora_salida': forms.TimeInput(attrs={'placeholder': 'Ej: 10:30'}),
            'hora_llegada': forms.TimeInput(attrs={'placeholder': 'Ej: 10:30'}),
            'estado' : forms.Select(choices=ESTADOS, attrs={'class':'form-select', 'aria-label':'Default select example'}),
            'descripcion': forms.Textarea(attrs={'rows':'3', 'cols':'40'})
        }
