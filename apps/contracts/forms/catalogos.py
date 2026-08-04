from django import forms
from ..models import Area, Empresa, TipoContrato

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            "nombre",
            "descripcion",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Nombre del área"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "rows": 3,
                "placeholder": "Descripción..."
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "rounded"
            }),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nombre",
            "nit",
            "direccion",
            "ciudad",
            "telefono",
            "correo",
            "pagina_web",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Nombre de la empresa"
            }),
            "nit": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "NIT"
            }),
            "direccion": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Dirección"
            }),
            "ciudad": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Ciudad"
            }),
            "telefono": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Teléfono"
            }),
            "correo": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "correo@empresa.com"
            }),
            "pagina_web": forms.URLInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "https://empresa.com"
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "rounded"
            }),
        }


class TipoContratoForm(forms.ModelForm):
    class Meta:
        model = TipoContrato
        fields = [
            "nombre",
            "descripcion",
            "activo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Nombre del tipo de contrato"
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "Descripción..."
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "rounded"
            }),
        }