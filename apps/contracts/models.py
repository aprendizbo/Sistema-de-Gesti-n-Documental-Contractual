import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Tercero(models.Model):
    TIPOS = [
        ("PROVEEDOR", "Proveedor"),
        ("CONTRATISTA", "Contratista"),
        ("CLIENTE", "Cliente"),
        ("PERSONA", "Persona Natural"),
        ("EMPLEADO", "Empleado"),
        ("ALIADO", "Aliado Estratégico"),
        ("OTRO", "Otro"),
    ]

    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='PROVEEDOR'
    )

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )

    identificacion = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="NIT / Documento"
    )

    direccion = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    # NUEVO: Fase 1
    ciudad = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    # Se mantiene igual para la Fase 2
    correo = models.EmailField(
        blank=True,
        null=True
    )

    # Se mantiene igual para la Fase 2 (futuro persona_contacto)
    contacto = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Persona de contacto (si aplica)"
    )

    # NUEVO: Fase 1
    cargo_contacto = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    # NUEVO: Fase 1 (Reemplaza a 'activo')
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="ACTIVO"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    
    # NUEVO: Fase 1
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
            "correo": self.correo,
            "contacto": self.contacto,
            "cargo_contacto": self.cargo_contacto,
            "estado": self.estado,
        }


class Area(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Área"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    activo = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.nombre


class TipoContrato(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Tipo de Contrato"
        verbose_name_plural = "Tipos de Contratos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RequisitoDocumental(models.Model):
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.CASCADE, related_name='requisitos')
    nombre_documento = models.CharField(max_length=150, verbose_name="Nombre del Documento Requerido")
    es_obligatorio = models.BooleanField(default=True, verbose_name="¿Es Obligatorio?")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Requisito Documental"
        verbose_name_plural = "Requisitos Documentales"
        unique_together = ('tipo_contrato', 'nombre_documento')

    def __str__(self):
        return f"{self.tipo_contrato.nombre} - {self.nombre_documento}"


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
    ]

    numero_contrato = models.CharField(max_length=50, unique=True, verbose_name="Número de Contrato")
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.PROTECT, related_name='contratos')
    
    empresa = models.CharField(max_length=200, verbose_name="Empresa / Contratista")
    nit = models.CharField(max_length=30, verbose_name="NIT / Identificación")
    
    tercero = models.ForeignKey(
        Tercero,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name="Tercero"
    )
    
    # Nuevos campos integrados
    area_destino = models.CharField(max_length=150, verbose_name="Área de Destino")
    
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name="Área Responsable"
    )
    
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contratos_a_cargo')
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Vencimiento")
    
    # Campos de alertas y correos
    tiempo_notificacion = models.IntegerField(choices=TIEMPO_NOTIFICACION_CHOICES, default=30, verbose_name="Anticipación de Notificación")
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
        """Calcula el porcentaje de cumplimiento de la plantilla documental."""
        requisitos = self.tipo_contrato.requisitos.filter(activo=True)
        total_requisitos = requisitos.count()
        if total_requisitos == 0:
            return 100
        
        docs_subidos = self.documentos.filter(requisito__in=requisitos, es_version_actual=True).values('requisito').distinct().count()
        return int((docs_subidos / total_requisitos) * 100)


def ruta_documento_contrato(instance, filename):
    """Organiza físicamente los archivos subidos en carpetas por número de contrato."""
    return f"contratos/{instance.contrato.numero_contrato}/{filename}"


class DocumentoContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='documentos')
    requisito = models.ForeignKey(RequisitoDocumental, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_archivo = models.CharField(max_length=200, verbose_name="Nombre del Archivo")
    archivo = models.FileField(
        upload_to=ruta_documento_contrato,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'zip'])],
        verbose_name="Archivo Adjunto"
    )
    version = models.PositiveIntegerField(default=1, verbose_name="Versión")
    es_version_actual = models.BooleanField(default=True, verbose_name="¿Es la versión actual?")
    
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento de Contrato"
        verbose_name_plural = "Documentos de Contratos"
        ordering = ['-version']

    def __str__(self):
        return f"{self.nombre_archivo} (v{self.version}) - {self.contrato.numero_contrato}"


class HistorialAuditoria(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación de Contrato'),
        ('SUBIR_DOC', 'Subió Documento'),
        ('ELIMINAR_DOC', 'Eliminó Documento'),
        ('RENOVAR', 'Renovó Contrato'),
        ('ALERTA', 'Envío de Alerta Automática'),
        ('MODIFICAR', 'Modificación de Datos'),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    descripcion = models.TextField(verbose_name="Descripción del cambio")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Auditoría"
        verbose_name_plural = "Historiales de Auditoría"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.fecha_registro.strftime('%d/%m/%Y %H:%M')} - {self.get_accion_display()} por {self.usuario or 'Sistema'}"