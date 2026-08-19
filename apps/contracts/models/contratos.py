from django.db import models
from django.contrib.auth.models import User

class Contrato(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('POR_VENCER', 'Próximo a Vencer'),
        ('VENCIDO', 'Vencido'),
        ('RENOVADO', 'Renovado'),
        ('PENDIENTE_DOC', 'Pendiente por Documentación'),
        ('FINALIZADO', 'Finalizado'),
    ]

    TIEMPO_NOTIFICACION_CHOICES = [
        (90, '90 días antes'),
        (30, '30 días antes'),
        (15, '15 días antes'),
        (5, '5 días antes'),
        (1, '1 día antes'),
    ]

    numero_contrato = models.CharField(max_length=50, unique=True, verbose_name="Número de Contrato")
    
    tipo_contrato = models.ForeignKey(
        'TipoContrato', 
        on_delete=models.PROTECT, 
        related_name='contratos'
    )
    
    empresa = models.CharField(max_length=200, verbose_name="Empresa / Contratista")
    nit = models.CharField(max_length=30, verbose_name="NIT / Identificación")
    
    tercero = models.ForeignKey(
        'Tercero',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name="Tercero"
    )
    
    area_destino = models.ForeignKey(
        'Area',
        on_delete=models.PROTECT,
        related_name="contratos_destino",
        verbose_name="Área de Destino"
    )
    
    area = models.ForeignKey(
        'Area',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name="Área Responsable"
    )
    
    responsable = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='contratos_a_cargo'
    )
    
    supervisor = models.ForeignKey(
        'Supervisor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contratos",
        verbose_name="Supervisor del Contrato"
    )
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Vencimiento")
    
    tiempo_notificacion = models.IntegerField(
        choices=TIEMPO_NOTIFICACION_CHOICES, 
        default=30, 
        verbose_name="Anticipación de Notificación"
    )
    
    correo_notificacion_principal = models.EmailField(
        verbose_name="Correo Principal"
    )
    
    correo_notificacion_secundario = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo Secundario"
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO', verbose_name="Estado")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    archivo_pdf = models.FileField(
        upload_to="contratos/",
        blank=True,
        null=True,
        verbose_name="Contrato PDF"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.numero_contrato} - {self.empresa}"

    @property
    def porcentaje_documentacion(self):
        """Calcula el porcentaje de cumplimiento de los documentos obligatorios."""
        # 1. Traer los requerimientos que sean OBLIGATORIOS para este tipo de contrato
        requisitos = self.tipo_contrato.documentos_requeridos.filter(obligatorio=True)
        total_requisitos = requisitos.count()
        
        if total_requisitos == 0:
            return 100
        
        # 2. Extraer los IDs de los tipos de documento que se requieren
        tipos_requeridos_ids = requisitos.values_list('tipo_documento_id', flat=True)
        
        # 3. Contar cuántos de esos tipos requeridos ya tienen al menos un archivo asociado al contrato
        docs_subidos = self.documentos.filter(
            tipo_documento_id__in=tipos_requeridos_ids
        ).values('tipo_documento').distinct().count()
        
        return int((docs_subidos / total_requisitos) * 100)


class NotificacionContrato(models.Model):

    TIPO_VENCIMIENTO = "VENCIMIENTO"

    TIPOS = [
        (TIPO_VENCIMIENTO, "Vencimiento contractual"),
    ]

    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="notificaciones",
        verbose_name="Contrato"
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS,
        default=TIPO_VENCIMIENTO
    )

    dias_anticipacion = models.PositiveIntegerField(
        verbose_name="Días de anticipación"
    )

    fecha_programada = models.DateField(
        verbose_name="Fecha programada"
    )

    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de envío"
    )

    enviada = models.BooleanField(
        default=False,
        verbose_name="Enviada"
    )

    leida = models.BooleanField(
        default=False,
        verbose_name="Leída"
    )

    error_envio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Error de envío"
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Notificación de Contrato"
        verbose_name_plural = "Notificaciones de Contratos"
        ordering = ["-creado_en"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "contrato",
                    "tipo",
                    "dias_anticipacion"
                ],
                name="unique_alerta_contrato_anticipacion"
            )
        ]

    def __str__(self):
        return (
            f"{self.contrato.numero_contrato} - "
            f"{self.dias_anticipacion} días"
        )