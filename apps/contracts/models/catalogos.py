from django.db import models


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

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().upper()

        if self.descripcion:
            self.descripcion = self.descripcion.strip()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class TipoContrato(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Tipo de contrato"
        verbose_name_plural = "Tipos de contrato"


class TipoDocumentoContractual(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    obligatorio = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tipo de Documento Contractual"
        verbose_name_plural = "Tipos de Documentos Contractuales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre