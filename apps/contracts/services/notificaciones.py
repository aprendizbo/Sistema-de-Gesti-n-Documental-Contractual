from datetime import date, timedelta
import re

from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from contracts.models import Contrato, NotificacionContrato


class ContratoNotificacionService:
    """
    Contiene la lógica relacionada con las notificaciones
    de vencimiento de contratos.
    """

    @staticmethod
    def contratos_proximos_a_vencer():
        """
        Obtiene los contratos que deben generar una notificación
        de vencimiento según la anticipación configurada.
        """

        hoy = date.today()

        contratos = Contrato.objects.filter(
            estado__in=["ACTIVO", "POR_VENCER"]
        )

        contratos_a_notificar = []

        for contrato in contratos:

            if not contrato.fecha_fin:
                continue

            dias_restantes = (
                contrato.fecha_fin - hoy
            ).days

            if dias_restantes == contrato.tiempo_notificacion:
                contratos_a_notificar.append(contrato)

        return contratos_a_notificar

    @staticmethod
    def crear_notificaciones_pendientes():
        """
        Crea las notificaciones internas de los contratos
        que están próximos a vencer.
        """

        hoy = date.today()

        contratos = Contrato.objects.filter(
            estado__in=["ACTIVO", "POR_VENCER"]
        )

        creadas = 0

        for contrato in contratos:

            if not contrato.fecha_fin:
                continue

            dias_restantes = (
                contrato.fecha_fin - hoy
            ).days

            if dias_restantes != contrato.tiempo_notificacion:
                continue

            _, creada = NotificacionContrato.objects.get_or_create(
                contrato=contrato,
                tipo=NotificacionContrato.TIPO_VENCIMIENTO,
                dias_anticipacion=contrato.tiempo_notificacion,
                defaults={
                    "fecha_programada": hoy,
                },
            )

            if creada:
                creadas += 1

        return creadas

    @staticmethod
    def obtener_nombre_destinatario(correo):
        """
        Convierte la parte inicial de un correo corporativo
        en un nombre o cargo legible para el saludo.
        """

        if not correo:
            return "USUARIO"

        nombre = correo.split("@")[0].lower()

        palabras = {
            "juridica": "JURÍDICA",
            "juridico": "JURÍDICO",
            "director": "DIRECTOR",
            "directora": "DIRECTORA",
            "jefe": "JEFE",
            "jefa": "JEFA",
            "gerente": "GERENTE",
            "gerencia": "GERENCIA",
            "presidente": "PRESIDENTE",
            "presidencia": "PRESIDENCIA",
            "asistente": "ASISTENTE",
            "secretaria": "SECRETARÍA",
            "secretario": "SECRETARIO",
            "contabilidad": "CONTABILIDAD",
            "financiera": "FINANCIERA",
            "financiero": "FINANCIERO",
            "recursos": "RECURSOS",
            "humanos": "HUMANOS",
            "talento": "TALENTO",
            "humano": "HUMANO",
            "compras": "COMPRAS",
            "comercial": "COMERCIAL",
            "ventas": "VENTAS",
            "administrativa": "ADMINISTRATIVA",
            "administrativo": "ADMINISTRATIVO",
            "sistemas": "SISTEMAS",
            "soporte": "SOPORTE",
            "ti": "TI",
            "tecnologia": "TECNOLOGÍA",
            "tecnologías": "TECNOLOGÍAS",
            "logistica": "LOGÍSTICA",
            "logística": "LOGÍSTICA",
            "talentohumano": "TALENTO HUMANO",
            "recursoshumanos": "RECURSOS HUMANOS",
            "jefegeneral": "JEFE GENERAL",
            "jefejuridico": "JEFE JURÍDICO",
            "jefejuridica": "JEFA JURÍDICA",
            "asistentejuridica": "ASISTENTE JURÍDICA",
            "asistentejuridico": "ASISTENTE JURÍDICO",
        }

        if nombre in palabras:
            return palabras[nombre]

        nombre_limpio = re.sub(
            r"[._-]+",
            " ",
            nombre
        )

        for palabra in sorted(
            palabras.keys(),
            key=len,
            reverse=True
        ):
            if palabra in nombre_limpio.replace(" ", ""):
                nombre_limpio = nombre_limpio.replace(
                    palabra,
                    palabras[palabra]
                )

        if not nombre_limpio.strip():
            return "USUARIO"

        return nombre_limpio.upper()

    @staticmethod
    def enviar_alerta(contrato):
        """
        Envía el correo de alerta de vencimiento.
        """

        asunto = (
            f"Alerta de vencimiento – "
            f"Contrato {contrato.numero_contrato}"
        )

        saludo = (
            ContratoNotificacionService
            .obtener_nombre_destinatario(
                contrato.correo_notificacion_principal
            )
        )

        dias_restantes = (
            contrato.fecha_fin - date.today()
        ).days

        mensaje = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alerta de vencimiento contractual</title>
</head>

<body style="margin:0; padding:0; background:#f3f6f9; font-family:Arial, Helvetica, sans-serif; color:#263238;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3f6f9; padding:35px 15px;">
        <tr>
            <td align="center">

                <table width="650" cellpadding="0" cellspacing="0" border="0"
                       style="max-width:650px; width:100%; background:#ffffff; border-radius:10px; overflow:hidden; border:1px solid #e1e7ed;">

                    <!-- ENCABEZADO -->
                    <tr>
                        <td style="background:#123B63; padding:28px 35px;">

                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>

                                    <td align="center" valign="middle">

                                        <img
                                            src="https://boccherinicol.vtexassets.com/assets/vtex.file-manager-graphql/images/117104a7-a9bf-4a1c-ba2b-c33ac4db466e___dc9a4962633b58475c7995a25825a981.jpg"
                                            alt="Boccherini S.A.S."
                                            width="180"
                                            style="display:block; width:180px; max-width:180px; height:auto; border:0; margin:0 auto;"
                                        >

                                        <div style="margin-top:12px; font-size:15px; color:#dce8f2; letter-spacing:0.3px;">
                                            Gestión Documental Contractual
                                        </div>

                                    </td>

                                </tr>
                            </table>

                        </td>
                    </tr>

                    <!-- BARRA DE ALERTA -->
                    <tr>
                        <td style="background:#fff7ed; border-bottom:1px solid #fed7aa; padding:18px 35px;">

                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>

                                    <td width="45" valign="top">
                                        <div style="width:32px; height:32px; line-height:32px; text-align:center; background:#f59e0b; color:#ffffff; border-radius:50%; font-size:18px; font-weight:bold;">
                                            !
                                        </div>
                                    </td>

                                    <td valign="middle">
                                        <div style="font-size:16px; font-weight:bold; color:#92400e;">
                                            Alerta de vencimiento contractual
                                        </div>

                                        <div style="margin-top:4px; font-size:13px; color:#78350f;">
                                            Se requiere revisar la situación del contrato en el sistema.
                                        </div>
                                    </td>

                                </tr>
                            </table>

                        </td>
                    </tr>

                    <!-- CONTENIDO -->
                    <tr>
                        <td style="padding:35px;">

                            <p style="margin:0 0 8px 0; font-size:15px; color:#374151;">
                                Hola <strong>{saludo}</strong>,
                            </p>

                            <p style="margin:0 0 25px 0; font-size:14px; line-height:1.7; color:#4b5563;">
                                El Sistema de Gestión Documental Contractual informa que
                                uno de los contratos registrados se encuentra próximo a vencer.
                            </p>

                            <!-- CONTRATO -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                   style="border:1px solid #dbe3ea; border-radius:8px; overflow:hidden;">

                                <tr>
                                    <td colspan="2"
                                        style="background:#f8fafc; padding:16px 18px; border-bottom:1px solid #dbe3ea;">

                                        <div style="font-size:12px; color:#6b7280; text-transform:uppercase; letter-spacing:0.5px;">
                                            Información del contrato
                                        </div>

                                        <div style="margin-top:5px; font-size:20px; font-weight:bold; color:#123B63;">
                                            {contrato.numero_contrato}
                                        </div>

                                    </td>
                                </tr>

                                <tr>
                                    <td width="45%"
                                        style="padding:15px 18px; border-bottom:1px solid #edf1f4; font-size:13px; color:#6b7280;">
                                        Empresa / Contratista
                                    </td>

                                    <td width="55%"
                                        style="padding:15px 18px; border-bottom:1px solid #edf1f4; font-size:14px; font-weight:bold; color:#263238;">
                                        {contrato.empresa or "No especificada"}
                                    </td>
                                </tr>

                                <tr>
                                    <td width="45%"
                                        style="padding:15px 18px; border-bottom:1px solid #edf1f4; font-size:13px; color:#6b7280;">
                                        Fecha de vencimiento
                                    </td>

                                    <td width="55%"
                                        style="padding:15px 18px; border-bottom:1px solid #edf1f4; font-size:14px; font-weight:bold; color:#b45309;">
                                        {contrato.fecha_fin.strftime('%d/%m/%Y')}
                                    </td>
                                </tr>

                                <tr>
                                    <td width="45%"
                                        style="padding:15px 18px; font-size:13px; color:#6b7280;">
                                        Días restantes
                                    </td>

                                    <td width="55%"
                                        style="padding:15px 18px; font-size:16px; font-weight:bold; color:#dc2626;">
                                        {dias_restantes} día{"s" if dias_restantes != 1 else ""}
                                    </td>
                                </tr>

                            </table>

                            <!-- ACCIÓN -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                   style="margin-top:25px;">

                                <tr>
                                    <td style="background:#eff6ff; border-left:4px solid #2563eb; padding:18px 20px;">

                                        <div style="font-size:14px; line-height:1.7; color:#374151;">
                                            Se solicita realizar oportunamente las gestiones
                                            correspondientes para la renovación o cierre del contrato,
                                            según aplique, con el fin de evitar interrupciones o riesgos
                                            asociados a su vencimiento.
                                        </div>

                                    </td>
                                </tr>

                            </table>

                            <!-- ACCESO AL SISTEMA -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                   style="margin-top:25px;">

                                <tr>
                                    <td align="center" style="padding:5px 0 10px 0;">

                                        <div style="font-size:13px; color:#6b7280; line-height:1.6;">
                                            Consulte el contrato y gestione las acciones correspondientes
                                            directamente desde <strong>Gestión Documental Pro</strong>.
                                        </div>

                                    </td>
                                </tr>

                            </table>

                            <!-- FIRMA -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0"
                                   style="margin-top:25px;">

                                <tr>
                                    <td style="border-top:1px solid #e5e7eb; padding-top:22px;">

                                        <div style="font-size:13px; color:#4b5563;">
                                            Atentamente,
                                        </div>

                                        <div style="margin-top:6px; font-size:14px; font-weight:bold; color:#123B63;">
                                            Sistema de Gestión Documental Contractual
                                        </div>

                                        <div style="margin-top:3px; font-size:13px; color:#6b7280;">
                                            Boccherini S.A.S.
                                        </div>

                                    </td>
                                </tr>

                            </table>

                        </td>
                    </tr>

                    <!-- PIE -->
                    <tr>
                        <td style="background:#f8fafc; border-top:1px solid #e5e7eb; padding:20px 35px;">

                            <p style="margin:0; font-size:11px; line-height:1.6; color:#6b7280; text-align:center;">
                                Este mensaje fue generado automáticamente por el Sistema de
                                Gestión Documental Contractual.
                                <br>
                                Por favor, no responda a este correo.
                            </p>

                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""

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

        correo = EmailMultiAlternatives(
            subject=asunto,
            body="Alerta de vencimiento contractual. Consulte la información del contrato en el sistema Gestión Documental Pro.",
            from_email=None,
            to=destinatarios,
        )

        correo.attach_alternative(
            mensaje,
            "text/html",
        )

        return correo.send()

    @staticmethod
    def procesar_alertas():
        """
        Procesa y envía las alertas de vencimiento.

        Este método está diseñado para ejecutarse cuando un usuario
        ingresa al sistema. No depende de Task Scheduler ni de un
        proceso externo del sistema operativo.
        """

        hoy = date.today()

        contratos = Contrato.objects.filter(
            estado__in=["ACTIVO", "POR_VENCER"]
        )

        enviadas = 0
        ya_enviadas = 0
        errores = 0

        for contrato in contratos:

            if not contrato.fecha_fin:
                continue

            if not contrato.correo_notificacion_principal:
                continue

            dias_anticipacion = contrato.tiempo_notificacion

            if not dias_anticipacion:
                continue

            fecha_programada = (
                contrato.fecha_fin
                - timedelta(days=dias_anticipacion)
            )

            if hoy < fecha_programada:
                continue

            notificacion, creada = (
                NotificacionContrato.objects.get_or_create(
                    contrato=contrato,
                    tipo=NotificacionContrato.TIPO_VENCIMIENTO,
                    dias_anticipacion=dias_anticipacion,
                    defaults={
                        "fecha_programada": fecha_programada,
                    },
                )
            )

            # Ya fue enviada anteriormente.
            if not creada and notificacion.enviada:
                ya_enviadas += 1
                continue

            try:

                ContratoNotificacionService.enviar_alerta(
                    contrato
                )

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

                enviadas += 1

            except Exception as e:

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

        return {
            "enviadas": enviadas,
            "ya_enviadas": ya_enviadas,
            "errores": errores,
        }