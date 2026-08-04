from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse  # <-- Import agregado HttpResponse

from contracts.models import Contrato, HistorialAuditoria, DocumentoContrato, TipoDocumento
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
    ).order_by(
        "tipo_documento__nombre",
        "-version"
    )

    return render(
        request,
        "contracts/contratos/detalle_contrato.html",
        {
            "contrato": contrato,
            "documentos": documentos,
        }
    )


@login_required
def crear_contrato(request):
    if request.method == "POST":
        # CAMBIO APLICADO AQUÍ: Se agregó request.FILES
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
        # CAMBIO APLICADO AQUÍ: Se agregó request.FILES
        form = ContratoForm(
            request.POST,
            request.FILES,
            instance=contrato
        )

        if form.is_valid():
            contrato = form.save(commit=False)
            
            # --- SE PUEDE APLICAR LA MISMA LÓGICA DE LECTURA AQUÍ SI ES NECESARIO ---
            # print(">>>> ENTRO A FORM VALID (EDITAR)")
            # if contrato.archivo_pdf:
            #    print(">>>> SI HAY PDF")
            #    print(">>>>", contrato.archivo_pdf)
            # else:
            #    print(">>>> NO HAY PDF")

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