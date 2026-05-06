"""WSGI config for domotica_iot project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "domotica_iot.settings")

application = get_wsgi_application()