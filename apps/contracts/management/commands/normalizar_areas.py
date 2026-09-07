from django.core.management.base import BaseCommand

from contracts.models import Area


class Command(BaseCommand):
    help = "Convierte los nombres de las áreas a MAYÚSCULAS."

    def handle(self, *args, **options):

        areas = Area.objects.all()

        for area in areas:
            nombre_anterior = area.nombre
            area.nombre = area.nombre.strip().upper()
            area.save(update_fields=["nombre"])

            self.stdout.write(
                f"{nombre_anterior} -> {area.nombre}"
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Se normalizaron {areas.count()} áreas."
            )
        )