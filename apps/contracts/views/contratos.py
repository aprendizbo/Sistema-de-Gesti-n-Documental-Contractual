from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from contracts.models import (
    Contrato,
    HistorialAuditoria,
    DocumentoContrato,
    TipoContratoDocumento,
)
from contracts.forms import ContratoForm


@login_required
def lista_contratos(request):
    contratos = Contrato.objects.all()

    return render(
        request,
        "contracts/contratos/lista_contratos.html",
        {
            "contratos": contratos
        }
    )


@login_required
def detalle_contrato(request, pk):
    contrato = get_object_or_404(
        Contrato,
        pk=pk
    )

    documentos = DocumentoContrato.objects.filter(
        contrato=contrato
    ).select_related(
        "tipo_documento"
    ).order_by(
        "tipo_documento_id",
        "version"
    )

    documentos_requeridos = TipoContratoDocumento.objects.filter(
        tipo_contrato=contrato.tipo_contrato
    ).select_related(
        "tipo_documento"
    ).order_by(
        "orden"
    )

    documentos_dict = {}

    for documento in documentos:
        documentos_dict.setdefault(
            documento.tipo_documento_id,
            []
        ).append(documento)

    return render(
        request,
        "contracts/contratos/detalle_contrato.html",
        {
            "contrato": contrato,
            "documentos_requeridos": documentos_requeridos,
            "documentos_dict": documentos_dict,
        }
    )


@login_required
def crear_contrato(request):
    if request.method == "POST":
        form = ContratoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            contrato = form.save(commit=False)

            if contrato.tercero:
                contrato.empresa = contrato.tercero.nombre
                contrato.nit = contrato.tercero.identificacion

            contrato.save()

            HistorialAuditoria.objects.create(
                contrato=contrato,
                usuario=request.user,
                accion="CREAR",
                descripcion=f"Se creó el contrato {contrato.numero_contrato} para la empresa {contrato.empresa}."
            )

            return redirect("contracts:lista")

    else:
        form = ContratoForm()

        return render(
            request,
            "contracts/contratos/crear_contrato.html",
            {
                "form": form
            }
        )


@login_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)

    if request.method == "POST":
        form = ContratoForm(
            request.POST,
            request.FILES,
            instance=contrato
        )

        if form.is_valid():
            contrato = form.save(commit=False)
            
            # Actualiza automáticamente la empresa y el NIT
            if contrato.tercero:
                contrato.empresa = contrato.tercero.nombre
                contrato.nit = contrato.tercero.identificacion

            contrato.save()

            HistorialAuditoria.objects.create(
                contrato=contrato,
                usuario=request.user,
                accion="MODIFICAR",
                descripcion=f"Se actualizó el contrato {contrato.numero_contrato}."
            )

            return redirect(
                "contracts:detalle_contrato",
                pk=contrato.pk
            )

    else:
        form = ContratoForm(instance=contrato)

    return render(
        request,
        "contracts/contratos/editar_contrato.html",
        {
            "form": form,
            "contrato": contrato
        }
    )


@login_required
def renovar_contrato(request, pk):
    contrato_anterior = get_object_or_404(
        Contrato,
        pk=pk
    )

    if request.method == "POST":
        form = ContratoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            nuevo_contrato = form.save(commit=False)

            if nuevo_contrato.tercero:
                nuevo_contrato.empresa = nuevo_contrato.tercero.nombre
                nuevo_contrato.nit = nuevo_contrato.tercero.identificacion

            nuevo_contrato.contrato_anterior = contrato_anterior
            nuevo_contrato.save()

            contrato_anterior.estado = "RENOVADO"
            contrato_anterior.save(update_fields=["estado"])

            HistorialAuditoria.objects.create(
                contrato=contrato_anterior,
                usuario=request.user,
                accion="RENOVAR",
                descripcion=(
                    f"El contrato {contrato_anterior.numero_contrato} "
                    f"fue renovado mediante el contrato "
                    f"{nuevo_contrato.numero_contrato}."
                )
            )

            HistorialAuditoria.objects.create(
                contrato=nuevo_contrato,
                usuario=request.user,
                accion="CREAR",
                descripcion=(
                    f"Se creó el contrato {nuevo_contrato.numero_contrato} "
                    f"como renovación del contrato "
                    f"{contrato_anterior.numero_contrato}."
                )
            )

            return redirect(
                "contracts:detalle_contrato",
                pk=nuevo_contrato.pk
            )

    else:
        form = ContratoForm(
            initial={
                "tipo_contrato": contrato_anterior.tipo_contrato,
                "tercero": contrato_anterior.tercero,
                "area_destino": contrato_anterior.area_destino,
                "area": contrato_anterior.area,
                "responsable": contrato_anterior.responsable,
                "supervisor": contrato_anterior.supervisor,
                "correo_notificacion_principal": (
                    contrato_anterior.correo_notificacion_principal
                ),
                "correo_notificacion_secundario": (
                    contrato_anterior.correo_notificacion_secundario
                ),
                "tiempo_notificacion": (
                    contrato_anterior.tiempo_notificacion
                ),
            }
        )

    return render(
        request,
        "contracts/contratos/renovar_contrato.html",
        {
            "form": form,
            "contrato_anterior": contrato_anterior,
        }
    )


@login_required
def finalizar_contrato(request, pk):
    contrato = get_object_or_404(
        Contrato,
        pk=pk
    )

    if request.method == "POST":
        contrato.estado = "FINALIZADO"
        contrato.save(update_fields=["estado"])

        HistorialAuditoria.objects.create(
            contrato=contrato,
            usuario=request.user,
            accion="FINALIZAR",
            descripcion=(
                f"El contrato {contrato.numero_contrato} "
                f"fue finalizado definitivamente."
            )
        )

        return redirect(
            "contracts:detalle_contrato",
            pk=contrato.pk
        )

    return redirect(
        "contracts:detalle_contrato",
        pk=contrato.pk
    )