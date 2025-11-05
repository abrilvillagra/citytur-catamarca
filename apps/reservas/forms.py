
from django import forms

from apps.reservas.models import Recorrido, PuntoTuristico,Reserva

from django.core.exceptions import ValidationError
from django.utils import timezone


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
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'Ej: 10:30', 'type': 'time', 'required':'required'}),
            'hora_llegada': forms.TimeInput(format='%H:%M',attrs={'placeholder': 'Ej: 10:30', 'type': 'time', 'required':'required'}),
            'descripcion': forms.Textarea(attrs={'rows':'3', 'cols':'35'}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-select'}),
            'puntos_turisticos': forms.SelectMultiple(attrs={'class':'form-select', 'size':'5'})
        }
    def __init__(self, *args, disable_estado=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['puntos_turisticos'].queryset = PuntoTuristico.objects.filter(estado=True)

        # Si la instancia no existe (creación) nos aseguramos de tener initial True
        if not getattr(self.instance, 'pk', None):
            self.initial.setdefault('estado', True)

        # Aplicar disabled si se solicita
        if disable_estado:
            self.fields['estado'].disabled = True

    def clean(self):
        cleaned_data=super().clean()
        hora_salida=cleaned_data.get('hora_salida')
        hora_llegada=cleaned_data.get('hora_llegada')

        if hora_salida and hora_llegada and hora_salida >= hora_llegada:
            raise ValidationError("La hora de llegada debe ser posterior a la hora de salida")
        return cleaned_data


class PuntoTuristaForm(forms.ModelForm):
    ESTADOS=[
        ('True', 'Activo'),
        ('False', 'Inactivo'),
    ]

    estado=forms.TypedChoiceField(
        choices=ESTADOS,
        coerce=lambda val:val=='True',
        widget=forms.Select(attrs={'class':'form-select','aria-label':'Default select example'}),
        required=False
    )

    class Meta:
        model=PuntoTuristico
        fields=['nombre', 'categoria', 'descripcion', 'ubicacion', 'estado']

        widgets={
            'nombre':forms.TextInput(attrs={'required':'required'}),
            'categoria':forms.Select(attrs={'class':'form-select'}),
            'descripcion':forms.Textarea(attrs={'rows':'3', 'cols':'35'}),
            'ubicacion':forms.TextInput(attrs={'required':'required'}),
        }


class ReservaForm(forms.ModelForm):
    # Opciones de forma de pago, como en el modelo
    FORMA_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
        ('QR', 'QR'),
    ]

    forma_de_pago = forms.ChoiceField(
        choices=FORMA_PAGO,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Forma de pago"
    )

    fecha_reserva = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat()
        }),
        label="Fecha de la reserva"
    )

    cantidad_personas = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 11)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Cantidad de pasajeros"
    )

    class Meta:
        model = Reserva
        fields = [
            'nombre_completo',
            'email',
            'telefono',
            'recorrido',
            'cantidad_personas',
            'fecha_reserva',
            'forma_de_pago'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre y apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@email.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3834000000'
            }),
            'recorrido': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo recorridos activos
        self.fields['recorrido'].queryset = Recorrido.objects.filter(estado=True)

    def clean_fecha_reserva(self):
        fecha = self.cleaned_data.get('fecha_reserva')
        if fecha and fecha < timezone.now().date():
            raise ValidationError("La fecha de reserva no puede ser anterior a hoy.")
        return fecha
