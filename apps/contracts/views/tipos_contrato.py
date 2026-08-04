from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from contracts.models import TipoContrato
from contracts.forms import TipoContratoForm


@login_required
def lista_tipos_contrato(request):
    tipos = TipoContrato.objects.all().order_by("nombre")

    return render(
        request,
        "contracts/tipos_contrato/lista.html",
        {
            "tipos": tipos
        }
    )


@login_required
def crear_tipo_contrato(request):
    if request.method == "POST":
        form = TipoContratoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contracts:lista_tipos_contrato")

    else:
        form = TipoContratoForm()

    return render(
        request,
        "contracts/tipos_contrato/crear.html",
        {
            "form": form
        }
    )


@login_required
def editar_tipo_contrato(request, pk):
    tipo = get_object_or_404(TipoContrato, pk=pk)

    if request.method == "POST":
        form = TipoContratoForm(
            request.POST,
            instance=tipo
        )

        if form.is_valid():
            form.save()
            return redirect("contracts:lista_tipos_contrato")

    else:
        form = TipoContratoForm(instance=tipo)

    return render(
        request,
        "contracts/tipos_contrato/crear.html",
        {
            "form": form,
            "tipo": tipo
        }
    )