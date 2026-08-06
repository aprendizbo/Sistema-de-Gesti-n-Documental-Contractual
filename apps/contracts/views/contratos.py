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
        documentos_dict[documento.tipo_documento_id] = documento

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