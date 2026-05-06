"""URL configuration for domotica_iot."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("devices/", include("devices.urls")),
    path("rules/", include("rules.urls")),
    path("events/", include("events.urls")),
]