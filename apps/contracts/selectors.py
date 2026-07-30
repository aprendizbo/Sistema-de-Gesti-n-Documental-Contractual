from django.db.models import Q

from .models import Tercero


class TerceroSelector:

    @staticmethod
    def listar():
        return Tercero.objects.all().order_by("nombre")

    @staticmethod
    def buscar(texto):
        return (
            Tercero.objects.filter(
                Q(nombre__icontains=texto)
                | Q(identificacion__icontains=texto)
                | Q(correo__icontains=texto)
                | Q(contacto__icontains=texto)
            )
            .order_by("nombre")
        )