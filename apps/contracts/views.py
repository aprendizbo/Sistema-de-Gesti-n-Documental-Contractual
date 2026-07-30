from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contrato, HistorialAuditoria, Tercero
from .forms import ContratoForm, TerceroForm
from .services import TerceroService


@login_required
def lista_contratos(request):
    # Consultamos todos los contratos de la base de datos
    contratos = Contrato.objects.all()
    
    context = {
        'contratos': contratos
    }
    return render(request, 'contratos/lista_contratos.html', context)


@login_required
def detalle_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    
    context = {
        'contrato': contrato
    }
    return render(request, 'contratos/detalle_contrato.html', context)


@login_required
def crear_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            
            # Registramos la acción en el Historial de Auditoría
            HistorialAuditoria.objects.create(
                contrato=contrato,
                usuario=request.user,
                accion='CREAR',
                descripcion=f"Se creó el contrato {contrato.numero_contrato} para la empresa {contrato.empresa}."
            )
            return redirect('contracts:lista')
    else:
        form = ContratoForm()
    
    context = {
        'form': form
    }
    return render(request, 'contratos/crear_contrato.html', context)


@login_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            contrato = form.save()
            
            # Registramos la acción en el Historial de Auditoría
            HistorialAuditoria.objects.create(
                contrato=contrato,
                usuario=request.user,
                accion='EDITAR',
                descripcion=f"Se actualizó el contrato {contrato.numero_contrato}."
            )
            return redirect('contracts:detalle_contrato', pk=contrato.pk)
    else:
        form = ContratoForm(instance=contrato)
    
    context = {
        'form': form,
        'contrato': contrato
    }
    return render(request, 'contratos/editar_contrato.html', context)


@login_required
def crear_tercero(request):
    if request.method == "POST":
        form = TerceroForm(request.POST)
        if form.is_valid():
            TerceroService.crear_tercero(form)
            return redirect("contracts:lista_terceros")
    else:
        form = TerceroForm()

    return render(
        request,
        "contratos/terceros/crear.html",
        {
            "form": form
        }
    )


@login_required
def lista_terceros(request):
    terceros = Tercero.objects.all().order_by("nombre")

    return render(
        request,
        "contratos/terceros/lista.html",
        {
            "terceros": terceros
        }
    )


@login_required
def editar_tercero(request, pk):
    tercero = get_object_or_404(Tercero, pk=pk)

    if request.method == "POST":
        form = TerceroForm(
            request.POST,
            instance=tercero
        )

        if form.is_valid():
            TerceroService.actualizar_tercero(form)
            return redirect("contracts:lista_terceros")

    else:
        form = TerceroForm(instance=tercero)

    return render(
        request,
        "contratos/terceros/crear.html",
        {
            "form": form,
            "tercero": tercero
        }
    )