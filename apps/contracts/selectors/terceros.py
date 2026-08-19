from contracts.models import Tercero


class TerceroSelector:
    """
    Consultas relacionadas con terceros.
    """

    @staticmethod
    def listar():
        return Tercero.objects.all().order_by("nombre")

    @staticmethod
    def buscar(busqueda):
        return Tercero.objects.filter(
            nombre__icontains=busqueda
        ).order_by("nombre")