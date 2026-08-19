from datetime import timedelta

from django.utils import timezone


ESTADOS_MANUALES = {
    "RENOVADO",
    "FINALIZADO",
}


def determinar_estado_contrato(contrato, fecha=None):
    """
    Determina automáticamente el estado contractual
    basándose en la fecha de vencimiento.

    Los estados RENOVADO y FINALIZADO son manuales
    y nunca serán modificados por esta lógica.
    """

    if fecha is None:
        fecha = timezone.localdate()

    # --------------------------------------------------
    # ESTADOS MANUALES
    # --------------------------------------------------

    if contrato.estado in ESTADOS_MANUALES:
        return contrato.estado

    # --------------------------------------------------
    # CONTRATO VENCIDO
    # --------------------------------------------------

    if contrato.fecha_fin < fecha:
        return "VENCIDO"

    # --------------------------------------------------
    # CONTRATO PRÓXIMO A VENCER
    # --------------------------------------------------

    limite_por_vencer = fecha + timedelta(days=90)

    if contrato.fecha_fin <= limite_por_vencer:
        return "POR_VENCER"

    # --------------------------------------------------
    # CONTRATO ACTIVO
    # --------------------------------------------------

    return "ACTIVO"


def actualizar_estado_contrato(contrato, guardar=True):
    """
    Calcula y actualiza el estado del contrato.

    Retorna el estado resultante.
    """

    nuevo_estado = determinar_estado_contrato(contrato)

    if contrato.estado != nuevo_estado:
        contrato.estado = nuevo_estado

        if guardar:
            contrato.save(update_fields=["estado", "actualizado_en"])

    return nuevo_estado


def actualizar_estados_contratos():
    """
    Actualiza automáticamente los estados de todos
    los contratos que no estén RENOVADOS o FINALIZADOS.

    Retorna la cantidad de contratos modificados.
    """

    from contracts.models import Contrato

    contratos = Contrato.objects.exclude(
        estado__in=ESTADOS_MANUALES
    )

    modificados = 0

    for contrato in contratos:

        nuevo_estado = determinar_estado_contrato(contrato)

        if contrato.estado != nuevo_estado:
            contrato.estado = nuevo_estado

            contrato.save(
                update_fields=[
                    "estado",
                    "actualizado_en",
                ]
            )

            modificados += 1

    return modificados