from django.db import models
from .Account import Account
from .Strategy import Strategy


class Snapshot(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    strategy = models.ForeignKey(
        Strategy, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.CharField(max_length=255)
    nav = models.DecimalField(max_digits=20, decimal_places=8)
    exposure = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "snapshots"

    def __str__(self):
        strategy_info = f" - {self.strategy.prefix}" if self.strategy else ""
        return f"{self.account.name}{strategy_info} ({self.event})"
