from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from contracts.models import NotificacionContrato


@login_required
def obtener_notificaciones(request):
    """
    Devuelve las notificaciones pendientes de lectura
    para mostrarlas en la campanita del sistema.
    """

    notificaciones = (
        NotificacionContrato.objects
        .filter(leida=False)
        .select_related("contrato")
        .order_by("-creado_en")[:10]
    )

    data = []

    for notificacion in notificaciones:

        contrato = notificacion.contrato

        # Calcular días restantes hasta el vencimiento
        dias_restantes = (
            contrato.fecha_fin - notificacion.fecha_programada
        ).days

        # Mensaje que verá el usuario
        if notificacion.dias_anticipacion == 1:
            mensaje = (
                f"El contrato {contrato.numero_contrato} "
                f"vence en 1 día."
            )
        else:
            mensaje = (
                f"El contrato {contrato.numero_contrato} "
                f"vence en {notificacion.dias_anticipacion} días."
            )

        data.append({
            "id": notificacion.id,
            "contrato_id": contrato.id,
            "numero_contrato": contrato.numero_contrato,

            "mensaje": mensaje,

            "dias_anticipacion": notificacion.dias_anticipacion,

            "fecha_vencimiento": (
                contrato.fecha_fin.strftime("%d/%m/%Y")
            ),

            "fecha_programada": (
                notificacion.fecha_programada.strftime("%d/%m/%Y")
            ),

            "enviada": notificacion.enviada,
            "leida": notificacion.leida,

            "url": (
                f"/contratos/contratos/{contrato.id}/"
            ),
        })

    return JsonResponse({
        "total": len(data),
        "notificaciones": data,
    })


@login_required
def marcar_notificacion_leida(request, pk):
    """
    Marca una notificación como leída.
    """

    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido."},
            status=405
        )

    notificacion = get_object_or_404(
        NotificacionContrato,
        pk=pk
    )

    notificacion.leida = True

    notificacion.save(
        update_fields=["leida"]
    )

    return JsonResponse({
        "success": True,
        "mensaje": "Notificación marcada como leída."
    })