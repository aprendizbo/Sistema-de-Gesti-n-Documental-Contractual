from django.db import models

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