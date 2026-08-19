from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from contracts.models import Contrato, NotificacionContrato
from contracts.services.estados import actualizar_estados_contratos
from contracts.services.notificaciones import ContratoNotificacionService


@login_required
def dashboard(request):

    actualizar_estados_contratos()
    ContratoNotificacionService.crear_notificaciones_pendientes()

    hoy = timezone.localdate()
    limite_90_dias = hoy + timedelta(days=90)

    # ==========================================================
    # CONTRATOS
    # ==========================================================

    total_contratos = Contrato.objects.count()

    contratos_activos = Contrato.objects.filter(
        estado="ACTIVO"
    ).count()

    contratos_renovados = Contrato.objects.filter(
        estado="RENOVADO"
    ).count()

    contratos_finalizados = Contrato.objects.filter(
        estado="FINALIZADO"
    ).count()

    # ==========================================================
    # VENCIDOS REALES
    # ==========================================================
    #
    # No dependemos únicamente del campo estado.
    # Si la fecha ya pasó, el contrato está vencido.
    #

    contratos_vencidos = Contrato.objects.filter(
        fecha_fin__lt=hoy
    ).exclude(
        estado="FINALIZADO"
    ).exclude(
        estado="RENOVADO"
    ).count()

    # ==========================================================
    # PRÓXIMOS A VENCER
    # ==========================================================
    #
    # Contratos cuya fecha de vencimiento está entre hoy y
    # los próximos 90 días.
    #

    contratos_por_vencer = Contrato.objects.filter(
        fecha_fin__gte=hoy,
        fecha_fin__lte=limite_90_dias
    ).exclude(
        estado="FINALIZADO"
    ).exclude(
        estado="RENOVADO"
    ).count()

    # ==========================================================
    # PENDIENTES DE DOCUMENTACIÓN
    # ==========================================================
    #
    # Utilizamos el porcentaje_documentacion que ya existe
    # en el model Contrato.
    #

    contratos = Contrato.objects.all()

    contratos_pendientes_documentacion = 0

    for contrato in contratos:
        if contrato.porcentaje_documentacion < 100:
            contratos_pendientes_documentacion += 1

    # ==========================================================
    # PRÓXIMOS VENCIMIENTOS
    # ==========================================================

    proximos_vencimientos = (
        Contrato.objects
        .filter(
            fecha_fin__gte=hoy,
            fecha_fin__lte=limite_90_dias,
        )
        .exclude(
            estado="FINALIZADO"
        )
        .exclude(
            estado="RENOVADO"
        )
        .select_related(
            "tipo_contrato",
            "tercero",
            "responsable",
            "area_destino",
            "supervisor",
        )
        .order_by("fecha_fin")[:10]
    )

    # ==========================================================
    # NOTIFICACIONES PENDIENTES
    # ==========================================================

    notificaciones_pendientes = (
        NotificacionContrato.objects
        .filter(leida=False)
        .select_related("contrato")
        .order_by("-creado_en")[:10]
    )

    total_notificaciones_pendientes = (
        NotificacionContrato.objects
        .filter(leida=False)
        .count()
    )

    # ==========================================================
    # CONTRATOS SIN DOCUMENTACIÓN COMPLETA
    # ==========================================================

    contratos_documentacion = []

    for contrato in contratos:
        porcentaje = contrato.porcentaje_documentacion

        if porcentaje < 100:
            contratos_documentacion.append({
                "contrato": contrato,
                "porcentaje": porcentaje,
            })

    contratos_documentacion.sort(
        key=lambda item: item["porcentaje"]
    )

    contratos_documentacion = contratos_documentacion[:10]

    # ==========================================================
    # CONTEXTO
    # ==========================================================

    context = {
        "hoy": hoy,

        # Estadísticas
        "total_contratos": total_contratos,
        "contratos_activos": contratos_activos,
        "contratos_por_vencer": contratos_por_vencer,
        "contratos_vencidos": contratos_vencidos,
        "contratos_pendientes_documentacion": contratos_pendientes_documentacion,
        "contratos_finalizados": contratos_finalizados,
        "contratos_renovados": contratos_renovados,

        # Vencimientos
        "proximos_vencimientos": proximos_vencimientos,

        # Documentación
        "contratos_documentacion": contratos_documentacion,

        # Notificaciones
        "notificaciones_pendientes": notificaciones_pendientes,
        "total_notificaciones_pendientes": total_notificaciones_pendientes,
    }

    return render(
        request,
        "core/dashboard.html",
        context
    )