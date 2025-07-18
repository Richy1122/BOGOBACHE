from django import forms
from .models import Bache, Localidad, UPZ, Barrio
from django.core.exceptions import ValidationError

class BacheForm(forms.ModelForm):
    latitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitud = forms.DecimalField(max_digits=9, decimal_places=6, required=True)
    
    class Meta:
        model = Bache
        fields = ['latitud', 'longitud', 'localidad', 'upz', 'barrio', 'estado',
                  'peligrosidad', 'tipo_calle', 'direccion', 'diametro', 'accidentes', 'foto']
        exclude = ['id_bache', 'created_at', 'updated_at', 'deleted_at']
        widgets = {
            'latitud': forms.NumberInput(attrs={'step': '0.000001', 'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'step': '0.000001', 'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'peligrosidad': forms.HiddenInput(),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'upz': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'barrio': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'diametro': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': '5 cm',
                'class': 'form-control'
            }),
            # 👇 Añade estos tres campos
            'tipo_calle': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].initial = 'sin_arreglar'  # ✅ Valor por defecto
        self.fields['diametro'].initial = 5
        self.fields['accidentes'].initial = 0
        self.fields['peligrosidad'].initial = 'Alto'

    def clean(self):
        cleaned_data = super().clean()
        latitud = cleaned_data.get('latitud')
        longitud = cleaned_data.get('longitud')
        diametro = cleaned_data.get('diametro')
        accidentes = cleaned_data.get('accidentes')

        if latitud and (latitud < 4.4 or latitud > 5.0):
            raise ValidationError({'latitud': 'La latitud debe estar dentro del rango de Bogotá'})
        if longitud and (longitud < -74.2 or longitud > -73.9):
            raise ValidationError({'longitud': 'La longitud debe estar dentro del rango de Bogotá'})
        if not latitud:
            raise ValidationError({'latitud': 'Debes seleccionar la ubicación en el mapa'})
        if not longitud:
            raise ValidationError({'longitud': 'Debes seleccionar la ubicación en el mapa'})
        
        if diametro is not None and diametro < 5:
            self.add_error('diametro', 'El diámetro del bache no puede ser menor a 5 cms')
        if accidentes not in [0, 1, '0', '1']:
            self.add_error('accidentes', 'Seleccione si sufrió un accidente')

        return cleaned_data
