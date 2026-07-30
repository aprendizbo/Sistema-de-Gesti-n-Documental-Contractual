from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from contracts.models import Area
from contracts.forms import AreaForm


@login_required
def lista_areas(request):
    areas = Area.objects.all().order_by("nombre")

    return render(
        request,
        "contracts/areas/lista.html",
        {
            "areas": areas
        }
    )


@login_required
def crear_area(request):

    if request.method == "POST":
        form = AreaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contracts:lista_areas")

    else:
        form = AreaForm()

    return render(
        request,
        "contracts/areas/crear.html",
        {
            "form": form
        }
    )


@login_required
def editar_area(request, pk):

    area = get_object_or_404(
        Area,
        pk=pk
    )

    if request.method == "POST":

        form = AreaForm(
            request.POST,
            instance=area
        )

        if form.is_valid():
            form.save()

            return redirect(
                "contracts:lista_areas"
            )

    else:

        form = AreaForm(
            instance=area
        )

    return render(
        request,
        "contracts/areas/crear.html",
        {
            "form": form,
            "area": area
        }
    )