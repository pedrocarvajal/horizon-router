from rest_framework import serializers
from core.models.strategy import Strategy


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = [
            "id",
            "name",
            "prefix",
            "symbol",
            "created_at",
            "updated_at",
        ]
