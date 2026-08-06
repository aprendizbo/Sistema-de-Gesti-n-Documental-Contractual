import os
from django.db import models


def ruta_documento_contrato(instance, filename):
    return os.path.join("contratos", "documentos", filename)


class TipoContratoDocumento(models.Model):
    tipo_contrato = models.ForeignKey(
        'TipoContrato',
        on_delete=models.CASCADE,
        related_name="documentos_requeridos"
    )

    tipo_documento = models.ForeignKey(
        'TipoDocumentoContractual',
        on_delete=models.CASCADE,
        related_name="tipos_contrato",
    )

    obligatorio = models.BooleanField(default=True)

    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.tipo_contrato} - {self.tipo_documento}"


class DocumentoContrato(models.Model):
    contrato = models.ForeignKey(
        'Contrato',
        on_delete=models.CASCADE,
        related_name="documentos"
    )

    tipo_documento = models.ForeignKey(
        'TipoDocumentoContractual',
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