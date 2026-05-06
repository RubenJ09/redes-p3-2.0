from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView, CreateView

from devices.forms import DeviceForm
from devices.models import Device


class DeviceListView(ListView):
    model = Device
    template_name = "devices/device_list.html"
    context_object_name = "devices"

class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = "devices/device_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dispositivo creado correctamente.")
        return response

    def get_success_url(self):
        return reverse("devices:list")


class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = "devices/device_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dispositivo actualizado correctamente.")
        return response

    def get_success_url(self):
        return reverse("devices:list")


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = "devices/device_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Dispositivo eliminado correctamente.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("devices:list")


def home_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("devices:list")