import json
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.heartbeat import Heartbeat
from core.models.account import Account
from core.models.strategy import Strategy
from core.helpers.response import response


@api_view(["POST"])
def create_heartbeat(request):
    schema = {
        "broker_account_number": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "strategy_prefix": {
            "type": "string",
            "required": True,
            "maxlength": 50,
            "empty": False,
        },
        "event": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
    }

    validator = Validator(schema)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return response(message="Invalid JSON format", status_code=400)

    if not validator.validate(data):
        return response(
            message="Validation failed", data=validator.errors, status_code=400
        )

    broker_account_number = data["broker_account_number"]
    strategy_prefix = data["strategy_prefix"]
    event = data["event"]

    try:
        account = Account.objects.get(broker_account_number=broker_account_number)
    except Account.DoesNotExist:
        return response(
            message=f"Account with broker_account_number {broker_account_number} does not exist",
            status_code=404,
        )

    try:
        strategy = Strategy.objects.get(prefix=strategy_prefix)
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with prefix {strategy_prefix} does not exist",
            status_code=404,
        )

    Heartbeat.objects.create(account=account, strategy=strategy, event=event)

    cutoff_date = timezone.now() - timedelta(days=7)
    Heartbeat.objects.filter(created_at__lt=cutoff_date).delete()

    return response(
        message="Heartbeat created successfully",
        status_code=201,
    )
