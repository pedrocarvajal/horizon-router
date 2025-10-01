from rest_framework import serializers
from core.models.deal import Deal


class DealSerializer(serializers.ModelSerializer):
    strategy = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    volume = serializers.CharField()
    price = serializers.CharField()
    profit = serializers.CharField()
    take_profit_price = serializers.CharField()
    stop_loss_price = serializers.CharField()

    class Meta:
        model = Deal
        fields = [
            "id",
            "token",
            "strategy",
            "time",
            "symbol",
            "type",
            "direction",
            "volume",
            "price",
            "profit",
            "take_profit_price",
            "stop_loss_price",
            "account",
            "created_at",
            "updated_at",
        ]

    def get_strategy(self, obj):
        return {
            "id": obj.strategy.id,
            "name": obj.strategy.name,
            "prefix": obj.strategy.prefix,
        }

    def get_account(self, obj):
        return {
            "id": obj.account.id,
            "name": obj.account.name,
        }
