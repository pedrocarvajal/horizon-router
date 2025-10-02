from django.db import models
from .account import Account
from .strategy import Strategy


class Deal(models.Model):
    token = models.CharField(max_length=255)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    time = models.DateTimeField()
    symbol = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    direction = models.IntegerField()
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit_price = models.DecimalField(
        max_digits=20, decimal_places=8, null=True, blank=True
    )
    stop_loss_price = models.DecimalField(
        max_digits=20, decimal_places=8, null=True, blank=True
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "deals"

    def __str__(self):
        return f"{self.strategy.prefix} - {self.symbol} ({self.type})"
