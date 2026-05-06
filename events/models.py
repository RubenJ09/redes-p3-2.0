from django.db import models


class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=64, blank=True, null=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"Evento de {self.device} a las {self.timestamp}"