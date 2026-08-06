from django import forms

from contracts.models import (
    TipoDocumentoContractual,
    TipoContratoDocumento,
)


class TipoDocumentoContractualForm(forms.ModelForm):

    class Meta:
        model = TipoDocumentoContractual

        fields = [
            "nombre",
            "descripcion",
            "obligatorio",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                    "placeholder": "Ej: Cámara de Comercio",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                    "rows": 4,
                    "placeholder": "Descripción del documento...",
                }
            ),
            "obligatorio": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500",
                }
            ),
        }


class TipoContratoDocumentoForm(forms.ModelForm):

    class Meta:
        model = TipoContratoDocumento

        fields = [
            "tipo_documento",
            "obligatorio",
            "orden",
        ]

        widgets = {
            "tipo_documento": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "obligatorio": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "orden": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),
        }