from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=50)
    symbol = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "strategies"

    def __str__(self):
        return f"{self.prefix} - {self.name}"
