import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def ruta_documento_contrato(instance, filename):
    return os.path.join("contratos", "documentos", filename)


class Empresa(models.Model):
    nombre = models.CharField(
        max_length=200,
        unique=True
    )
    nit = models.CharField(
        max_length=50,
        unique=True
    )
    direccion = models.CharField(
        max_length=250,
        blank=True
    )
    ciudad = models.CharField(
        max_length=120,
        blank=True
    )
    telefono = models.CharField(
        max_length=50,
        blank=True
    )
    correo = models.EmailField(
        blank=True
    )
    pagina_web = models.URLField(
        blank=True
    )
    activo = models.BooleanField(
        default=True
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.nombre} ({self.nit})"


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

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name="terceros",
        null=True,
        blank=True
    )

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

    correo = models.EmailField(
        blank=True,
        null=True
    )

    contacto = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Persona de contacto (si aplica)"
    )

    cargo_contacto = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="ACTIVO"
    )

    creado_en = models.DateTimeField(auto_now_add=True)
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
            "empresa": self.empresa.nombre if self.empresa else "",
            "tipo": self.tipo,
            "estado": self.estado,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "ciudad": self.ciudad,
            "telefono": self.telefono,
            "correo": self.correo,
            "contacto": self.contacto,
            "cargo_contacto": self.cargo_contacto,
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


class Supervisor(models.Model):
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre"
    )

    cargo = models.CharField(
        max_length=120,
        blank=True
    )

    correo = models.EmailField(
        unique=True
    )

    telefono = models.CharField(
        max_length=30,
        blank=True
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="supervisores",
        verbose_name="Empresa",
        null=True,
        blank=True,
    )

    activo = models.BooleanField(
        default=True
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"

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
    
    area_destino = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="contratos_destino",
        verbose_name="Área de Destino"
    )
    
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name="Área Responsable"
    )
    
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contratos_a_cargo')
    
    supervisor = models.ForeignKey(
        Supervisor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contratos",
        verbose_name="Supervisor del Contrato"
    )
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Vencimiento")
    
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
        """Calcula el porcentaje de cumplimiento de la plantilla documental."""
        requisitos = self.tipo_contrato.requisitos.filter(activo=True)
        total_requisitos = requisitos.count()
        if total_requisitos == 0:
            return 100
        
        docs_subidos = self.documentos.filter(requisito__in=requisitos, es_version_actual=True).values('requisito').distinct().count()
        return int((docs_subidos / total_requisitos) * 100)


class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    obligatorio = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class DocumentoContrato(models.Model):
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="documentos"
    )

    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name="documentos",
        null=True,
        blank=True,
    )

    archivo = models.FileField(
        upload_to=ruta_documento_contrato
    )

    version = models.PositiveIntegerField(default=1)

    observaciones = models.TextField(blank=True)

    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento del Contrato"
        verbose_name_plural = "Documentos de Contratos"
        ordering = ["tipo_documento"]

    def __str__(self):
        return f"{self.contrato.numero_contrato} - {self.tipo_documento.nombre if self.tipo_documento else 'Sin tipo'}"


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
        return f"{self.fecha_registro.strftime('%d/%m/%Y %H:%M')} - {self.get_accion_display()} por {self.usuario or 'Sistema'} en contrato {self.contrato.numero_contrato}"