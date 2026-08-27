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
    ContratoNotificacionService.procesar_alertas()

    hoy = timezone.localdate()
    limite_90_dias = hoy + timedelta(days=90)

    # ==========================================================
    # CONTRATOS ACTUALES
    # ==========================================================
    
    contratos_actuales = Contrato.objects.exclude(
        estado__in=["RENOVADO", "FINALIZADO"]
    )

    contratos_activos_lista = contratos_actuales.filter(
        estado="ACTIVO"
    ).select_related(
        "tipo_contrato",
        "tercero",
        "area_destino",
        "responsable",
        "supervisor",
    ).order_by("fecha_fin")

    contratos_por_vencer_lista = contratos_actuales.filter(
        fecha_fin__gte=hoy,
        fecha_fin__lte=limite_90_dias
    ).select_related(
        "tipo_contrato",
        "tercero",
        "area_destino",
        "responsable",
        "supervisor",
    ).order_by("fecha_fin")

    contratos_vencidos_lista = contratos_actuales.filter(
        fecha_fin__lt=hoy
    ).select_related(
        "tipo_contrato",
        "tercero",
        "area_destino",
        "responsable",
        "supervisor",
    ).order_by("-fecha_fin")
    
    total_contratos = contratos_actuales.count()
    
    contratos_activos = contratos_actuales.filter(
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

    contratos_vencidos = contratos_actuales.filter(
        fecha_fin__lt=hoy
    ).count()

    # ==========================================================
    # PRÓXIMOS A VENCER
    # ==========================================================

    contratos_por_vencer = contratos_actuales.filter(
        fecha_fin__gte=hoy,
        fecha_fin__lte=limite_90_dias
    ).count()

    # ==========================================================
    # PENDIENTES DE DOCUMENTACIÓN
    # ==========================================================
    #
    # Utilizamos el porcentaje_documentacion que ya existe
    # en el model Contrato.
    #

    contratos = contratos_actuales

    contratos_pendientes_documentacion = 0

    for contrato in contratos:
        if contrato.porcentaje_documentacion < 100:
            contratos_pendientes_documentacion += 1

    # ==========================================================
    # LISTADOS ADICIONALES PARA DASHBOARD
    # ==========================================================

    contratos_renovados_lista = (
        Contrato.objects
        .filter(estado="RENOVADO")
        .select_related(
            "tipo_contrato",
            "tercero",
            "contrato_anterior",
        )
        .order_by("-fecha_fin")
    )

    contratos_finalizados_lista = (
        Contrato.objects
        .filter(estado="FINALIZADO")
        .select_related(
            "tipo_contrato",
            "tercero",
            "contrato_anterior",
        )
        .order_by("-fecha_fin")
    )

    # ==========================================================
    # PRÓXIMOS VENCIMIENTOS
    # ==========================================================

    proximos_vencimientos = (
        contratos_actuales
        .filter(
            fecha_fin__gte=hoy,
            fecha_fin__lte=limite_90_dias,
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
        
        # Listas para el dashboard interactivo
        "contratos_actuales": contratos_actuales,
        "contratos_activos_lista": contratos_activos_lista,
        "contratos_por_vencer_lista": contratos_por_vencer_lista,
        "contratos_vencidos_lista": contratos_vencidos_lista,
        "contratos_renovados_lista": contratos_renovados_lista,
        "contratos_finalizados_lista": contratos_finalizados_lista,

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