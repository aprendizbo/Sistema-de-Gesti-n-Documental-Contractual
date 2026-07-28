from django.core.mail import send_mail
from django.conf import settings

def enviar_alerta_vencimiento_contrato(contrato):
    """
    Envía una notificación formal de próximo vencimiento de contrato 
    al correo principal administrativo y al correo opcional si existe.
    """
    asunto = f"[ALERTA CLM] Próximo Vencimiento - Contrato Nº {contrato.numero_contrato}"
    
    mensaje = f"""Estimado equipo administrativo,

Se le informa de manera formal que el contrato descrito a continuación se encuentra próximo a vencer según el tiempo de anticipación configurado.

A continuación, los detalles del contrato:

- Número de Contrato: {contrato.numero_contrato}
- Tipo de Contrato: {contrato.tipo_contrato.nombre}
- Empresa / Contratista: {contrato.empresa}
- NIT / Identificación: {contrato.nit}
- Área de Destino: {contrato.area_destino}
- Responsable Asignado: {contrato.responsable.get_full_name() if contrato.responsable else 'No asignado'}
- Fecha de Vencimiento: {contrato.fecha_fin.strftime('%d/%m/%Y')}

Por favor, tomar las medidas necesarias para la gestión documental, revisión o renovación oportuna de este acuerdo.

Atentamente,
Sistema de Gestión Documental Contractual - CLM Pro
"""

    # Construir lista de destinatarios (Obligatorio principal + Opcional si está lleno)
    destinatarios = [contrato.correo_notificacion_principal]
    if contrato.correo_notificacion_opcional:
        destinatarios.append(contrato.correo_notificacion_opcional)

    # Enviar correo electrónico
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=False,
    )