from django.core.management.base import BaseCommand
from django.db import transaction

from contracts.models import (
    Contrato,
    NotificacionContrato,
    DocumentoContrato,
    HistorialAuditoria,
    Empresa,
    Tercero,
    Supervisor,
    TipoContrato,
    TipoContratoDocumento,
    TipoDocumentoContractual,
    Area,
)


class Command(BaseCommand):
    help = "Limpia los datos de prueba y conserva las áreas."

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "INICIANDO LIMPIEZA DE DATOS DE PRODUCCIÓN"
            )
        )
        self.stdout.write("")

        # =====================================================
        # MOSTRAR DATOS ANTES DE BORRAR
        # =====================================================

        self.stdout.write("DATOS ANTES DE LA LIMPIEZA:")
        self.stdout.write(
            f"Contratos: {Contrato.objects.count()}"
        )
        self.stdout.write(
            f"Notificaciones: {NotificacionContrato.objects.count()}"
        )
        self.stdout.write(
            f"Documentos: {DocumentoContrato.objects.count()}"
        )
        self.stdout.write(
            f"Historiales: {HistorialAuditoria.objects.count()}"
        )
        self.stdout.write(
            f"Empresas: {Empresa.objects.count()}"
        )
        self.stdout.write(
            f"Terceros: {Tercero.objects.count()}"
        )
        self.stdout.write(
            f"Supervisores: {Supervisor.objects.count()}"
        )
        self.stdout.write(
            f"Tipos de contrato: {TipoContrato.objects.count()}"
        )
        self.stdout.write(
            f"Relaciones tipo contrato/documento: "
            f"{TipoContratoDocumento.objects.count()}"
        )
        self.stdout.write(
            f"Tipos de documento: "
            f"{TipoDocumentoContractual.objects.count()}"
        )
        self.stdout.write(
            f"Áreas a conservar: {Area.objects.count()}"
        )

        self.stdout.write("")

        # =====================================================
        # LIMPIEZA
        # =====================================================

        self.stdout.write(
            self.style.WARNING(
                "Eliminando datos..."
            )
        )

        # -----------------------------------------------------
        # 1. Contratos
        # -----------------------------------------------------
        #
        # Al eliminar los contratos, Django elimina
        # automáticamente:
        #
        # - NotificacionContrato
        # - DocumentoContrato
        # - HistorialAuditoria
        #
        # porque utilizan on_delete=models.CASCADE.
        # -----------------------------------------------------

        Contrato.objects.all().delete()

        # -----------------------------------------------------
        # 2. Relaciones entre tipos de contrato y documentos
        # -----------------------------------------------------

        TipoContratoDocumento.objects.all().delete()

        # -----------------------------------------------------
        # 3. Tipos de contrato
        # -----------------------------------------------------

        TipoContrato.objects.all().delete()

        # -----------------------------------------------------
        # 4. Tipos de documentos contractuales
        # -----------------------------------------------------

        TipoDocumentoContractual.objects.all().delete()

        # -----------------------------------------------------
        # 5. Supervisores
        # -----------------------------------------------------

        Supervisor.objects.all().delete()

        # -----------------------------------------------------
        # 6. Terceros
        # -----------------------------------------------------

        Tercero.objects.all().delete()

        # -----------------------------------------------------
        # 7. Empresas
        # -----------------------------------------------------

        Empresa.objects.all().delete()

        # =====================================================
        # IMPORTANTE:
        #
        # NO TOCAR Area
        # =====================================================

        # Las áreas se conservan.

        # =====================================================
        # VERIFICACIÓN FINAL
        # =====================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "LIMPIEZA COMPLETADA"
            )
        )
        self.stdout.write("")

        self.stdout.write("DATOS DESPUÉS DE LA LIMPIEZA:")

        self.stdout.write(
            f"Contratos: {Contrato.objects.count()}"
        )
        self.stdout.write(
            f"Notificaciones: {NotificacionContrato.objects.count()}"
        )
        self.stdout.write(
            f"Documentos: {DocumentoContrato.objects.count()}"
        )
        self.stdout.write(
            f"Historiales: {HistorialAuditoria.objects.count()}"
        )
        self.stdout.write(
            f"Empresas: {Empresa.objects.count()}"
        )
        self.stdout.write(
            f"Terceros: {Tercero.objects.count()}"
        )
        self.stdout.write(
            f"Supervisores: {Supervisor.objects.count()}"
        )
        self.stdout.write(
            f"Tipos de contrato: {TipoContrato.objects.count()}"
        )
        self.stdout.write(
            f"Relaciones tipo contrato/documento: "
            f"{TipoContratoDocumento.objects.count()}"
        )
        self.stdout.write(
            f"Tipos de documento: "
            f"{TipoDocumentoContractual.objects.count()}"
        )
        self.stdout.write(
            f"Áreas conservadas: {Area.objects.count()}"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Las áreas NO fueron eliminadas."
            )
        )