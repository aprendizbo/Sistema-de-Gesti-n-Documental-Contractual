from django import forms
from ..models import Supervisor

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = [
            "empresa",
            "nombre",
            "cargo",
            "correo",
            "telefono",
            "activo",
        ]
        widgets = {
            "empresa": forms.Select(attrs={
                "class": "w-full px-4 py-2 border rounded-lg"
            }),
            "nombre": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Nombre completo"
            }),
            "cargo": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Ej: Coordinador Jurídico"
            }),
            "correo": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "usuario@boccherini.com.co"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "3001234567"
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "rounded"
            }),
        }