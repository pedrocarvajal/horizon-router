import json
from rest_framework.decorators import api_view
from cerberus import Validator
from models.Heartbeat import Heartbeat
from models.Account import Account
from models.Strategy import Strategy
from helpers.response import response


@api_view(["POST"])
def create_heartbeat(request):
    # Validation
    schema = {
        "account_id": {
            "type": "integer",
            "required": True,
            "min": 1,
        },
        "strategy_id": {
            "type": "integer",
            "required": True,
            "min": 1,
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

    account_id = data["account_id"]
    strategy_id = data["strategy_id"]
    event = data["event"]

    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return response(
            message=f"Account with id {account_id} does not exist", status_code=404
        )

    try:
        strategy = Strategy.objects.get(id=strategy_id)
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with id {strategy_id} does not exist", status_code=404
        )

    # Logic
    Heartbeat.objects.create(account=account, strategy=strategy, event=event)

    return response(
        message="Heartbeat created successfully",
        status_code=201,
    )
