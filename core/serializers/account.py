from rest_framework import serializers
from core.models.account import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "broker_account_number",
            "broker_name",
            "created_at",
            "updated_at",
        ]
