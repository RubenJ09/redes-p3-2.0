from django import forms

from devices.models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["device_id", "name", "device_type", "topic", "command_topic", "current_state"]

    def clean(self):
        cleaned_data = super().clean()
        device_type = cleaned_data.get("device_type")
        command_topic = cleaned_data.get("command_topic")
        topic = cleaned_data.get("topic")

        if device_type == Device.DeviceType.SWITCH and not command_topic and topic:
            cleaned_data["command_topic"] = f"{topic}/set"

        return cleaned_data