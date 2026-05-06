from django.db import models


class Rule(models.Model):
    raw_text = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.raw_text