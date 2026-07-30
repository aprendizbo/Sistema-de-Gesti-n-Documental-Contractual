from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from contracts.models import Tercero
from contracts.forms import TerceroForm
from contracts.services import TerceroService
from contracts.selectors import TerceroSelector  # <-- Nueva importación agregada


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
        "contracts/terceros/crear.html",
        {
            "form": form
        }
    )


@login_required
def lista_terceros(request):
    busqueda = request.GET.get("q")
    
    if busqueda:
        terceros = TerceroSelector.buscar(busqueda)
    else:
        terceros = TerceroSelector.listar()

    return render(
        request,
        "contracts/terceros/lista.html",
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
        "contracts/terceros/crear.html",
        {
            "form": form,
            "tercero": tercero
        }
    )


@login_required
def obtener_tercero(request, pk):
    tercero = get_object_or_404(Tercero, pk=pk)

    return JsonResponse({
        "nombre": tercero.nombre,
        "identificacion": tercero.identificacion,
        "ciudad": tercero.ciudad,
        "contacto": tercero.contacto,
        "correo": tercero.correo,
    })