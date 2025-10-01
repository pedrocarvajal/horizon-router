from rest_framework import serializers
from core.models.snapshot import Snapshot


class SnapshotSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    strategy = serializers.SerializerMethodField()
    nav = serializers.CharField()
    exposure = serializers.CharField()

    class Meta:
        model = Snapshot
        fields = [
            "id",
            "account",
            "strategy",
            "event",
            "nav",
            "exposure",
            "created_at",
            "updated_at",
        ]

    def get_account(self, obj):
        return {
            "id": obj.account.id,
            "name": obj.account.name,
        }

    def get_strategy(self, obj):
        if obj.strategy:
            return {
                "id": obj.strategy.id,
                "name": obj.strategy.name,
                "prefix": obj.strategy.prefix,
            }
        return None
