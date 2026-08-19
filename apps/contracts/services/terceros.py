class TerceroService:
    """
    Contiene toda la lógica relacionada con los terceros.
    """

    @staticmethod
    def crear_tercero(form):
        """
        Crea un tercero y devuelve la instancia creada.
        """
        return form.save()

    @staticmethod
    def actualizar_tercero(form):
        """
        Actualiza un tercero existente.
        """
        return form.save()