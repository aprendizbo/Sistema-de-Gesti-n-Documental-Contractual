from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from contracts.models import Empresa
from contracts.forms import EmpresaForm


@login_required
def lista_empresas(request):

    empresas = Empresa.objects.all().order_by("nombre")

    return render(
        request,
        "contracts/empresas/lista.html",
        {
            "empresas": empresas
        }
    )


@login_required
def crear_empresa(request):

    if request.method == "POST":

        form = EmpresaForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("contracts:lista_empresas")

    else:

        form = EmpresaForm()

    return render(
        request,
        "contracts/empresas/crear.html",
        {
            "form": form
        }
    )


@login_required
def editar_empresa(request, pk):

    empresa = get_object_or_404(
        Empresa,
        pk=pk
    )

    if request.method == "POST":

        form = EmpresaForm(
            request.POST,
            instance=empresa
        )

        if form.is_valid():

            form.save()

            return redirect(
                "contracts:lista_empresas"
            )

    else:

        form = EmpresaForm(
            instance=empresa
        )

    return render(
        request,
        "contracts/empresas/crear.html",
        {
            "form": form,
            "empresa": empresa
        }
    )