from django import forms
from ..models import Tercero

class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = [
            'empresa', 
            'tipo',
            'nombre',
            'identificacion',
            'direccion',
            'ciudad',
            'telefono',
            'correo',
            'contacto',
            'cargo_contacto',
            'estado',
        ]

        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Nombre del tercero'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'NIT o Documento'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Dirección'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Ciudad'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Teléfono de contacto'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'correo@dominio.com'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Nombre de la persona de contacto'
            }),
            'cargo_contacto': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Cargo de la persona de contacto'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }