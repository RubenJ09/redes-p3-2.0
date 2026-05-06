from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from devices.models import Device
from rules.models import Rule
from events.models import Event


BASE_TOPIC = "redes2/2311/04"


class Command(BaseCommand):
    help = "Carga datos de ejemplo para la demostración local de la práctica."

    def handle(self, *args, **options):
        try:
            Device.objects.update_or_create(
                device_id="switch_caldera",
                defaults={
                    "name": "Caldera",
                    "device_type": Device.DeviceType.SWITCH,
                    "topic": f"{BASE_TOPIC}/switch_caldera",
                    "command_topic": f"{BASE_TOPIC}/switch_caldera/set",
                    "current_state": "OFF",
                },
            )
            Device.objects.update_or_create(
                device_id="sensor_salon",
                defaults={
                    "name": "Sensor salón",
                    "device_type": Device.DeviceType.SENSOR,
                    "topic": f"{BASE_TOPIC}/sensor_salon",
                    "current_state": "24",
                },
            )
            Device.objects.update_or_create(
                device_id="clock_salon",
                defaults={
                    "name": "Reloj salón",
                    "device_type": Device.DeviceType.CLOCK,
                    "topic": f"{BASE_TOPIC}/clock_salon",
                    "current_state": "08:00:00",
                },
            )

            Rule.objects.update_or_create(
                raw_text="si sensor_salon mayor que 25 entonces switch_caldera OFF",
                defaults={"enabled": True},
            )
            Rule.objects.update_or_create(
                raw_text="si clock_salon == 08:00:00 entonces switch_caldera ON",
                defaults={"enabled": True},
            )

            Event.objects.update_or_create(
                device="sensor_salon",
                defaults={
                    "value": "26",
                    "description": "Evento demo: sensor_salon 26",
                },
            )
            Event.objects.update_or_create(
                device="clock_salon",
                defaults={
                    "value": "08:00:00",
                    "description": "Evento demo: clock_salon 08:00:00",
                },
            )
            Event.objects.update_or_create(
                device="switch_caldera",
                defaults={
                    "value": "OFF",
                    "description": "Estado inicial demo: switch_caldera OFF",
                },
            )

        except OperationalError as exc:
            raise SystemExit("Error: Ejecuta primero 'python manage.py migrate'.") from exc

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados correctamente."))