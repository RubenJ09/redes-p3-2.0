"""ASGI config for domotica_iot project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "domotica_iot.settings")

application = get_asgi_application()