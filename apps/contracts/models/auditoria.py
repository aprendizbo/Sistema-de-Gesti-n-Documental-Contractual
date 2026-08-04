from django.db import models
from django.contrib.auth.models import User

class HistorialAuditoria(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación de Contrato'),
        ('SUBIR_DOC', 'Subió Documento'),
        ('ELIMINAR_DOC', 'Eliminó Documento'),
        ('RENOVAR', 'Renovó Contrato'),
        ('ALERTA', 'Envío de Alerta Automática'),
        ('MODIFICAR', 'Modificación de Datos'),
    ]

    contrato = models.ForeignKey(
        'Contrato', 
        on_delete=models.CASCADE, 
        related_name='historial'
    )
    
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    accion = models.CharField(max_length=20, choices=ACCIONES)
    
    descripcion = models.TextField(verbose_name="Descripción del cambio")
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Auditoría"
        verbose_name_plural = "Historiales de Auditoría"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.fecha_registro.strftime('%d/%m/%Y %H:%M')} - {self.get_accion_display()} por {self.usuario or 'Sistema'} en contrato {self.contrato.numero_contrato}"