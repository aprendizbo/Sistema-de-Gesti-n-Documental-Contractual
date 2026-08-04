from django import forms
from ..models import Contrato

DOMINIOS_PERMITIDOS = [
    "boccherini.com.co",
]

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'numero_contrato', 
            'tipo_contrato', 
            'tercero',
            'supervisor',        
            'area_destino',      
            'area',              
            'responsable', 
            'fecha_inicio', 
            'fecha_fin', 
            'tiempo_notificacion',
            'correo_notificacion_principal',
            'correo_notificacion_secundario', 
            'estado', 
            'observaciones'
        ]
        widgets = {
            'numero_contrato': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Ej: CTR-2026-00125'
            }),
            'tipo_contrato': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'tercero': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'supervisor': forms.Select(attrs={  
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'area_destino': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'area': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'responsable': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'tiempo_notificacion': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'correo_notificacion_principal': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'admin.contratos@boccherini.com.co'
            }),
            'correo_notificacion_secundario': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'usuario.responsable@boccherini.com.co' 
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Observaciones adicionales...'
            }),
        }

    def _validar_dominio(self, correo):
        dominio = correo.split("@")[-1].lower()
        if dominio not in DOMINIOS_PERMITIDOS:
            raise forms.ValidationError(
                "Solo se permiten correos institucionales."
            )

    def clean(self):
        cleaned_data = super().clean()

        principal = cleaned_data.get("correo_notificacion_principal")
        secundario = cleaned_data.get("correo_notificacion_secundario")

        if principal:
            self._validar_dominio(principal)

        if secundario:
            self._validar_dominio(secundario)

        return cleaned_data