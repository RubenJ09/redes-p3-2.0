from django.db import models


class Device(models.Model):
    class DeviceType(models.TextChoices):
        SWITCH = "switch", "Interruptor"
        SENSOR = "sensor", "Sensor"
        CLOCK = "clock", "Reloj"

    device_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    device_type = models.CharField(max_length=16, choices=DeviceType.choices)
    topic = models.CharField(max_length=255)
    command_topic = models.CharField(max_length=255, blank=True)
    current_state = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["device_id"]

    def __str__(self) -> str:
        return f"{self.device_id} ({self.name})"