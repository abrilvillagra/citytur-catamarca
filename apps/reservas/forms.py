
from django import forms

from apps.reservas.models import Recorrido, PuntoTuristico

from django.core.exceptions import ValidationError

class RecorridoForm(forms.ModelForm):

    ESTADOS = [
        (True, 'Activo'),
        (False, 'Inactivo'),
    ]
    estado=forms.TypedChoiceField(choices=ESTADOS,
                                  coerce=lambda val: val=='True',
                                  widget=forms.Select(attrs={'class':'form-select','aria-label':'Default select example'}),
                                  required=False)


    class Meta:
        model=Recorrido
        fields=['nombre', 'precio', 'hora_salida', 'hora_llegada', 'estado', 'descripcion', 'imagen', 'puntos_turisticos']

        widgets={
            'nombre': forms.TextInput(attrs={'required':'required'}),
            'precio': forms.NumberInput(attrs={'min':'1', 'required':'required'}),
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'Ej: 10:30', 'type': 'time'}),
            'hora_llegada': forms.TimeInput(format='%H:%M',attrs={'placeholder': 'Ej: 10:30', 'type': 'time'}),
            'descripcion': forms.Textarea(attrs={'rows':'3', 'cols':'40'}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-select'}),
            'puntos_turisticos': forms.SelectMultiple(attrs={'class':'form-select', 'size':'5'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['puntos_turisticos'].queryset = PuntoTuristico.objects.filter(estado=True)

    def clean(self):
        cleaned_data=super().clean()
        hora_salida=cleaned_data.get('hora_salida')
        hora_llegada=cleaned_data.get('hora_llegada')

        if hora_salida and hora_llegada and hora_salida >= hora_llegada:
            raise ValidationError("La hora de llegada debe ser posterior a la hora de salida")
        return cleaned_data