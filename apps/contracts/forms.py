from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'numero_contrato', 
            'tipo_contrato', 
            'empresa', 
            'nit', 
            'area_destino',
            'responsable', 
            'fecha_inicio', 
            'fecha_fin', 
            'tiempo_notificacion',
            'correo_notificacion_principal',
            'correo_notificacion_opcional',
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
            'empresa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Nombre de la empresa o contratista'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Ej: 900123456-7'
            }),
            'area_destino': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Ej: Gestión Humana / Legal / TI'
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
            'correo_notificacion_opcional': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'usuario.responsable@correo.com (Opcional)'
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

    def clean_correo_notificacion_principal(self):
        correo = self.cleaned_data.get('correo_notificacion_principal')
        if correo and not correo.endswith('@boccherini.com.co'):
            raise forms.ValidationError("El correo principal debe pertenecer obligatoriamente al dominio institucional (@boccherini.com.co).")
        return correo