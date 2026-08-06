from django.shortcuts import render, get_object_or_404, redirect

from ..models import (
    TipoContrato,
    TipoContratoDocumento,
)
from ..forms.documentos import TipoContratoDocumentoForm


def lista_plantillas(request):

    tipos = TipoContrato.objects.all()

    return render(
        request,
        "contracts/plantillas/lista.html",
        {
            "tipos": tipos,
        }
    )


def detalle_plantilla(request, tipo_id):

    tipo = get_object_or_404(
        TipoContrato,
        pk=tipo_id,
    )

    if request.method == "POST":

        form = TipoContratoDocumentoForm(request.POST)

        if form.is_valid():

            nuevo = form.save(commit=False)
            nuevo.tipo_contrato = tipo
            nuevo.save()

            return redirect(
                "contracts:detalle_plantilla",
                tipo_id=tipo.id
            )

    else:

        form = TipoContratoDocumentoForm()

    documentos = TipoContratoDocumento.objects.filter(
        tipo_contrato=tipo
    ).order_by("orden")

    return render(
        request,
        "contracts/plantillas/detalle.html",
        {
            "tipo": tipo,
            "documentos": documentos,
            "form": form,
        }
    )