from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # <-- Importación agregada

from contracts.models import Supervisor
from contracts.forms import SupervisorForm


@login_required
def lista_supervisores(request):

    supervisores = Supervisor.objects.all().order_by("nombre")

    return render(
        request,
        "contracts/supervisores/lista.html",
        {
            "supervisores": supervisores
        }
    )


@login_required
def crear_supervisor(request):

    if request.method == "POST":

        form = SupervisorForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("contracts:lista_supervisores")

    else:

        form = SupervisorForm()

    return render(
        request,
        "contracts/supervisores/crear.html",
        {
            "form": form
        }
    )


@login_required
def editar_supervisor(request, pk):

    supervisor = get_object_or_404(
        Supervisor,
        pk=pk
    )

    if request.method == "POST":

        form = SupervisorForm(
            request.POST,
            instance=supervisor
        )

        if form.is_valid():

            form.save()

            return redirect(
                "contracts:lista_supervisores"
            )

    else:

        form = SupervisorForm(
            instance=supervisor
        )

    return render(
        request,
        "contracts/supervisores/crear.html",
        {
            "form": form,
            "supervisor": supervisor
        }
    )


# ==========================================
# NUEVA VISTA: Obtener Supervisor (JSON)
# ==========================================
@login_required
def obtener_supervisor(request, pk):

    supervisor = get_object_or_404(
        Supervisor,
        pk=pk
    )

    return JsonResponse({

        "nombre": supervisor.nombre,
        "cargo": supervisor.cargo,
        "correo": supervisor.correo,
        "telefono": supervisor.telefono,
        "empresa": supervisor.empresa.nombre if supervisor.empresa else "",
        "activo": "Activo" if supervisor.activo else "Inactivo",

    })