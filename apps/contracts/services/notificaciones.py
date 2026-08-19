from datetime import date
import re

from django.core.mail import EmailMessage
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
Hola {saludo},

Por medio de la presente, le informamos que el contrato relacionado
a continuación se encuentra próximo a vencer.

INFORMACIÓN DEL CONTRATO

Número de contrato: {contrato.numero_contrato}

Empresa / Contratista: {contrato.empresa or "No especificada"}

Fecha de vencimiento: {contrato.fecha_fin.strftime('%d/%m/%Y')}

Días restantes para el vencimiento: {dias_restantes}

Le solicitamos realizar las gestiones necesarias para su renovación
o cierre, según corresponda, con el fin de evitar interrupciones
o riesgos asociados al vencimiento del contrato.

Quedamos atentos a cualquier inquietud.

Atentamente,

Sistema de Gestión Documental Contractual
Boccherini S.A.S.

Este mensaje fue generado automáticamente por el Sistema de
Gestión Documental Contractual. Por favor, no responda a este correo.
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

        correo = EmailMessage(
            subject=asunto,
            body=mensaje,
            from_email=None,
            to=destinatarios,
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

            dias_restantes = (
                contrato.fecha_fin - hoy
            ).days

            dias_anticipacion = (
                contrato.tiempo_notificacion
            )

            if dias_restantes != dias_anticipacion:
                continue

            notificacion, creada = (
                NotificacionContrato.objects.get_or_create(
                    contrato=contrato,
                    tipo=NotificacionContrato.TIPO_VENCIMIENTO,
                    dias_anticipacion=dias_anticipacion,
                    defaults={
                        "fecha_programada": hoy,
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