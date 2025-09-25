from django.db import models
from .account import Account
from .strategy import Strategy


class Heartbeat(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    event = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "heartbeats"

    def __str__(self):
        return f"{self.account.name} - {self.strategy.prefix} ({self.event})"