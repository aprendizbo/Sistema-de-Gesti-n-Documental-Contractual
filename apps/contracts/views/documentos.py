from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from contracts.models import (
    Contrato,
    DocumentoContrato,
    TipoDocumentoContractual,  # <-- CAMBIO 1: Import actualizado
)
from contracts.forms.documentos import TipoDocumentoContractualForm


@login_required
def lista_tipos_documento(request):
    # <-- CAMBIO 2: .objects.all() actualizado
    documentos = TipoDocumentoContractual.objects.all().order_by("nombre")

    return render(
        request,
        "contracts/tipos_documento/lista.html",
        {
            "documentos": documentos,
        },
    )


@login_required
def crear_tipo_documento(request):
    if request.method == "POST":
        form = TipoDocumentoContractualForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contracts:lista_tipos_documento")
    else:
        form = TipoDocumentoContractualForm()

    return render(
        request,
        "contracts/tipos_documento/crear.html",
        {
            "form": form,
        },
    )


@login_required
def editar_tipo_documento(request, pk):
    # <-- CAMBIO 3: get_object_or_404 actualizado
    documento = get_object_or_404(
        TipoDocumentoContractual,
        pk=pk,
    )

    if request.method == "POST":
        form = TipoDocumentoContractualForm(
            request.POST,
            instance=documento,
        )

        if form.is_valid():
            form.save()
            return redirect("contracts:lista_tipos_documento")

    else:
        form = TipoDocumentoContractualForm(
            instance=documento,
        )

    return render(
        request,
        "contracts/tipos_documento/crear.html",
        {
            "form": form,
            "documento": documento,
        },
    )


@login_required
def subir_documento(request, pk):
    contrato = get_object_or_404(
        Contrato,
        pk=pk,
    )

    if request.method == "POST":
        print("===== SUBIR DOCUMENTO =====")
        print(request.POST)
        print(request.FILES)

        archivo = request.FILES.get("archivo")
        tipo = request.POST.get("tipo_documento")
        observaciones = request.POST.get("observaciones")

        print("TIPO:", tipo)
        print("ARCHIVO:", archivo)

        if archivo:
            ultima_version = DocumentoContrato.objects.filter(
                contrato=contrato,
                tipo_documento_id=tipo,
            ).order_by("-version").first()

            version = 1

            if ultima_version:
                version = ultima_version.version + 1

            DocumentoContrato.objects.create(
                contrato=contrato,
                archivo=archivo,
                tipo_documento_id=tipo,
                observaciones=observaciones,
                version=version,
            )

    return redirect(
        "contracts:detalle_contrato",
        pk=contrato.pk,
    )