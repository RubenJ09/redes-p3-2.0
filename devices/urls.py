from django.urls import path

from devices.views import DeviceCreateView, DeviceDeleteView, DeviceListView, DeviceUpdateView, home_redirect

app_name = "devices"

urlpatterns = [
    path("", home_redirect, name="home"),
    path("list/", DeviceListView.as_view(), name="list"),
    path("create/", DeviceCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", DeviceUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", DeviceDeleteView.as_view(), name="delete"),
]