import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from rules.mqtt_service import MQTTControllerService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Arranca el controlador MQTT de la práctica."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--host", default=settings.MQTT_HOST, help="Host del broker MQTT")
        parser.add_argument("--port", type=int, default=settings.MQTT_PORT, help="Puerto del broker MQTT")
        parser.add_argument("--base-topic", default=settings.MQTT_BASE_TOPIC, help="Topic base")
        parser.add_argument("--database", default="db.sqlite3", help="Nombre del fichero de base de datos SQLite")

    def handle(self, *args, **options):
        service = MQTTControllerService(
            host=options["host"], 
            port=options["port"], 
            base_topic=options["base_topic"]
        )

        self.stdout.write(self.style.SUCCESS(f"Controller iniciado en {options['host']}:{options['port']}"))
        self.stdout.write(self.style.SUCCESS(f"Usando base de datos: {options['database']}"))
        
        try:
            service.start()
        except KeyboardInterrupt:
            service.stop()
            self.stdout.write(self.style.WARNING("\nController detenido por el usuario."))
