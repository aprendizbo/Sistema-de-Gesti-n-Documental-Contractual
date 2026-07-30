from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from contracts.models import Contrato, HistorialAuditoria
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
    contrato = get_object_or_404(Contrato, pk=pk)

    return render(
        request,
        "contracts/contratos/detalle_contrato.html",
        {
            "contrato": contrato
        }
    )


@login_required
def crear_contrato(request):
    if request.method == "POST":
        form = ContratoForm(request.POST)

        if form.is_valid():
            contrato = form.save(commit=False)

            # Completa automáticamente la información desde el tercero
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