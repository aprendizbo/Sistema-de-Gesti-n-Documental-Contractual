from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from contracts.models import Contrato

class Command(BaseCommand):
    help = 'Revisa los contratos próximos a vencer y envía alertas por correo electrónico.'

    def handle(self, *args, **options):
        hoy = date.today()
        contratos = Contrato.objects.all()
        
        enviados = 0
        for contrato in contratos:
            if not contrato.fecha_fin:
                continue
                
            # Calculamos la fecha en que se debe enviar la alerta según los días de anticipación
            dias_anticipacion = getattr(contrato, 'tiempo_notificacion', 30)
            
            # Si el contrato ya venció o está dentro del rango de notificación
            delta_dias = (contrato.fecha_fin - hoy).days
            
            if 0 <= delta_dias <= int(dias_anticipacion):
                asunto = f"[ALERTA CLM] Contrato No. {contrato.numero_contrato} próximo a vencer"
                
                mensaje = (
                    f"Estimado equipo,\n\n"
                    f"Se le notifica que el siguiente contrato está próximo a su fecha de vencimiento:\n\n"
                    f"- Número de Contrato: {contrato.numero_contrato}\n"
                    f"- Tipo de Contrato: {contrato.tipo_contrato}\n"
                    f"- Empresa / Contratista: {contrato.empresa}\n"
                    f"- NIT: {contrato.nit}\n"
                    f"- Área de Destino: {contrato.area_destino}\n"
                    f"- Responsable Asignado: {contrato.responsable}\n"
                    f"- Fecha de Vencimiento: {contrato.fecha_fin.strftime('%d/%m/%Y')}\n\n"
                    f"Por favor gestione la renovación o cierre oportuno.\n\n"
                    f"Atentamente,\n"
                    f"Sistema CLM Pro"
                )
                
                # Recolectar destinatarios (El principal definido por el administrador y el opcional si existe)
                destinatarios = [contrato.correo_notificacion_principal]
                if contrato.correo_notificacion_opcional:
                    destinatarios.append(contrato.correo_notificacion_opcional)
                
                try:
                    send_mail(
                        subject=asunto,
                        message=mensaje,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=destinatarios,
                        fail_silently=False,
                    )
                    enviados += 1
                    self.stdout.write(self.style.SUCCESS(f"Alerta enviada para el contrato {contrato.numero_contrato} a {destinatarios}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al enviar correo para {contrato.numero_contrato}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Proceso finalizado. Total de alertas enviadas: {enviados}"))