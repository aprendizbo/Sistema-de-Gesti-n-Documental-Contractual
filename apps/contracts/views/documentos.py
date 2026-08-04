from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from contracts.models import (
    Contrato,
    DocumentoContrato,
    TipoDocumento,
)
@login_required
def subir_documento(request, pk):

    contrato = get_object_or_404(
        Contrato,
        pk=pk
    )

    if request.method == "POST":

        archivo = request.FILES.get("archivo")
        tipo = request.POST.get("tipo_documento")
        observaciones = request.POST.get("observaciones")

        if archivo:

            DocumentoContrato.objects.create(
                contrato=contrato,
                archivo=archivo,
                tipo_documento_id=tipo,
                observaciones=observaciones,
            )

    return redirect(
        "contracts:detalle_contrato",
        pk=contrato.pk
    )