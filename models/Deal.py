from django.db import models


class Deal(models.Model):
    token = models.CharField(max_length=255)
    strategy_prefix = models.CharField(max_length=50)
    time = models.DateTimeField()
    symbol = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    direction = models.IntegerField()
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "deals"

    def __str__(self):
        return f"{self.strategy_prefix} - {self.symbol} ({self.type})"
