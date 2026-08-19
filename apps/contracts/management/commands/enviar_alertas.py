from datetime import date
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

from contracts.models import Contrato, NotificacionContrato


class Command(BaseCommand):
    help = "Revisa contratos próximos a vencer, envía alertas y registra las notificaciones."

    def handle(self, *args, **options):

        hoy = date.today()

        contratos = Contrato.objects.all()

        enviados = 0
        ya_enviadas = 0
        errores = 0

        for contrato in contratos:

            # ==================================================
            # VALIDACIONES
            # ==================================================

            if not contrato.fecha_fin:
                continue

            if not contrato.correo_notificacion_principal:
                self.stdout.write(
                    self.style.WARNING(
                        f"{contrato.numero_contrato}: "
                        "sin correo de notificación principal."
                    )
                )
                continue

            # ==================================================
            # CONFIGURACIÓN DE LA ALERTA
            # ==================================================

            dias_anticipacion = int(
                contrato.tiempo_notificacion or 30
            )

            dias_restantes = (
                contrato.fecha_fin - hoy
            ).days

            # La alerta se genera únicamente el día exacto
            # configurado por el usuario.
            if dias_restantes != dias_anticipacion:
                continue

            # ==================================================
            # REGISTRO DE NOTIFICACIÓN
            # ==================================================

            notificacion, creada = NotificacionContrato.objects.get_or_create(
                contrato=contrato,
                tipo=NotificacionContrato.TIPO_VENCIMIENTO,
                dias_anticipacion=dias_anticipacion,
                defaults={
                    "fecha_programada": hoy,
                }
            )

            # Si ya fue enviada, no volver a enviarla.
            if not creada and notificacion.enviada:

                ya_enviadas += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"{contrato.numero_contrato}: "
                        f"alerta de {dias_anticipacion} días "
                        "ya fue enviada anteriormente."
                    )
                )

                continue

            # ==================================================
            # INFORMACIÓN DEL CONTRATO
            # ==================================================

            numero_contrato = contrato.numero_contrato
            tipo_contrato = contrato.tipo_contrato
            empresa = contrato.empresa
            nit = contrato.nit
            area = contrato.area_destino
            responsable = contrato.responsable

            fecha_vencimiento = contrato.fecha_fin.strftime(
                "%d/%m/%Y"
            )

            if dias_restantes == 1:
                texto_dias = "1 día"
            else:
                texto_dias = f"{dias_restantes} días"

            # ==================================================
            # CORREO
            # ==================================================

            asunto = (
                f"[CLM Pro] Alerta de vencimiento contractual "
                f"– {numero_contrato}"
            )

            mensaje = f"""
Cordial saludo,

Se ha generado una alerta de vencimiento contractual en el Sistema CLM Pro.

INFORMACIÓN DEL CONTRATO

Número de contrato: {numero_contrato}
Tipo de contrato: {tipo_contrato}
Empresa / Contratista: {empresa}
NIT / Identificación: {nit}
Área de destino: {area}
Responsable: {responsable}

INFORMACIÓN DE VENCIMIENTO

Fecha de vencimiento: {fecha_vencimiento}
Vencimiento en: {texto_dias}

Se recomienda gestionar oportunamente la renovación, prórroga o cierre del contrato, según corresponda, con el fin de garantizar la continuidad y el adecuado control de las obligaciones contractuales.

Este mensaje fue generado automáticamente por el Sistema CLM Pro.
Por favor, no responda directamente a este correo.

Atentamente,

Sistema CLM Pro
Gestión Documental Contractual
Boccherini S.A.S.
""".strip()

            # ==================================================
            # DESTINATARIOS
            # ==================================================

            destinatarios = [
                contrato.correo_notificacion_principal
            ]

            if (
                contrato.correo_notificacion_secundario
                and contrato.correo_notificacion_secundario
                not in destinatarios
            ):
                destinatarios.append(
                    contrato.correo_notificacion_secundario
                )

            # ==================================================
            # ENVÍO
            # ==================================================

            try:

                send_mail(
                    subject=asunto,
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=destinatarios,
                    fail_silently=False,
                )

                # ==================================================
                # ACTUALIZAR NOTIFICACIÓN
                # ==================================================

                notificacion.fecha_programada = hoy
                notificacion.fecha_envio = timezone.now()
                notificacion.enviada = True
                notificacion.error_envio = None
                notificacion.save(
                    update_fields=[
                        "fecha_programada",
                        "fecha_envio",
                        "enviada",
                        "error_envio",
                    ]
                )

                enviados += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Alerta enviada correctamente: "
                        f"{numero_contrato} → "
                        f"{', '.join(destinatarios)}"
                    )
                )

            except Exception as e:

                # ==================================================
                # REGISTRAR ERROR
                # ==================================================

                notificacion.fecha_programada = hoy
                notificacion.enviada = False
                notificacion.error_envio = str(e)
                notificacion.save(
                    update_fields=[
                        "fecha_programada",
                        "enviada",
                        "error_envio",
                    ]
                )

                errores += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Error enviando alerta para "
                        f"{numero_contrato}: {e}"
                    )
                )

        # ==================================================
        # RESULTADO
        # ==================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "PROCESO DE ALERTAS FINALIZADO"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Alertas enviadas: {enviados}"
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f"Alertas ya enviadas: {ya_enviadas}"
            )
        )
        self.stdout.write(
            self.style.ERROR(
                f"Errores: {errores}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )