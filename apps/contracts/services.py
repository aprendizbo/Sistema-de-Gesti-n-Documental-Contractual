from .models import Tercero


class TerceroService:
    """
    Contiene toda la lógica relacionada con los terceros.
    """

    @staticmethod
    def crear_tercero(form):
        """
        Crea un tercero y devuelve la instancia creada.
        """
        tercero = form.save()

        return tercero

    @staticmethod
    def actualizar_tercero(form):
        """
        Actualiza un tercero existente.
        """
        tercero = form.save()

        return tercero