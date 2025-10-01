import json
from datetime import datetime
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.deal import Deal
from core.models.strategy import Strategy
from core.models.account import Account
from core.helpers.response import response
from core.enums.deal import DealTypes, DealDirections
from core.serializers.deal import DealSerializer


@api_view(["POST"])
def create_deal(request):
    schema = {
        "token": {
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
        "strategy_name": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "time": {
            "type": "string",
            "required": True,
            "empty": False,
        },
        "symbol": {
            "type": "string",
            "required": True,
            "maxlength": 100,
            "empty": False,
        },
        "type": {
            "type": "integer",
            "required": True,
            "allowed": [DealTypes.ORDER_TYPE_BUY, DealTypes.ORDER_TYPE_SELL],
        },
        "direction": {
            "type": "integer",
            "required": True,
            "allowed": [DealDirections.IN, DealDirections.OUT],
        },
        "volume": {
            "type": "number",
            "required": True,
        },
        "price": {
            "type": "number",
            "required": True,
        },
        "profit": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "take_profit_price": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "stop_loss_price": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "broker_account_number": {
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

    try:
        strategy = Strategy.objects.get(prefix=data["strategy_prefix"])
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with prefix '{data['strategy_prefix']}' and name '{data['strategy_name']}' does not exist",
            status_code=404,
        )

    try:
        account = Account.objects.get(
            broker_account_number=data["broker_account_number"]
        )
    except Account.DoesNotExist:
        return response(
            message=f"Account with broker_account_number {data['broker_account_number']} does not exist",
            status_code=404,
        )

    try:
        time = datetime.fromisoformat(data["time"].replace("Z", "+00:00"))
    except ValueError:
        return response(
            message="Invalid time format. Use ISO 8601 format", status_code=400
        )

    deal = Deal.objects.create(
        token=data["token"],
        strategy=strategy,
        time=time,
        symbol=data["symbol"],
        type=data["type"],
        direction=data["direction"],
        volume=data["volume"],
        price=data["price"],
        profit=data.get("profit"),
        take_profit_price=data.get("take_profit_price"),
        stop_loss_price=data.get("stop_loss_price"),
        account=account,
    )

    return response(
        message="Deal created successfully",
        data={"id": deal.id},
        status_code=201,
    )


@api_view(["GET"])
def search_deals(request):
    deal_id = request.GET.get("id")
    deals = Deal.objects.select_related("strategy", "account")

    if deal_id:
        deals = deals.filter(id=deal_id)
    else:
        deals = deals.all()

    serializer = DealSerializer(deals, many=True)
    deals_data = serializer.data

    return response(
        message="Deals retrieved successfully",
        data=deals_data,
        status_code=200,
    )


@api_view(["PUT"])
def update_deal(request, deal_id):
    schema = {
        "token": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "strategy_id": {
            "type": "integer",
            "required": False,
        },
        "time": {
            "type": "string",
            "required": False,
            "empty": False,
        },
        "symbol": {
            "type": "string",
            "required": False,
            "maxlength": 100,
            "empty": False,
        },
        "type": {
            "type": "integer",
            "required": False,
            "allowed": [DealTypes.ORDER_TYPE_BUY, DealTypes.ORDER_TYPE_SELL],
        },
        "direction": {
            "type": "integer",
            "required": False,
            "allowed": [DealDirections.IN, DealDirections.OUT],
        },
        "volume": {
            "type": "number",
            "required": False,
        },
        "price": {
            "type": "number",
            "required": False,
        },
        "profit": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "take_profit_price": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "stop_loss_price": {
            "type": "number",
            "required": False,
            "nullable": True,
        },
        "broker_account_number": {
            "type": "string",
            "required": False,
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

    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        return response(
            message=f"Deal with id {deal_id} does not exist", status_code=404
        )

    if "strategy_id" in data:
        try:
            strategy = Strategy.objects.get(id=data["strategy_id"])
            deal.strategy = strategy
        except Strategy.DoesNotExist:
            return response(
                message=f"Strategy with id {data['strategy_id']} does not exist",
                status_code=404,
            )

    if "broker_account_number" in data:
        try:
            account = Account.objects.get(
                broker_account_number=data["broker_account_number"]
            )
            deal.account = account
        except Account.DoesNotExist:
            return response(
                message=f"Account with broker_account_number {data['broker_account_number']} does not exist",
                status_code=404,
            )

    if "time" in data:
        try:
            deal.time = datetime.fromisoformat(data["time"].replace("Z", "+00:00"))
        except ValueError:
            return response(
                message="Invalid time format. Use ISO 8601 format", status_code=400
            )

    if "token" in data:
        deal.token = data["token"]
    if "symbol" in data:
        deal.symbol = data["symbol"]
    if "type" in data:
        deal.type = data["type"]
    if "direction" in data:
        deal.direction = data["direction"]
    if "volume" in data:
        deal.volume = data["volume"]
    if "price" in data:
        deal.price = data["price"]
    if "profit" in data:
        deal.profit = data["profit"]
    if "take_profit_price" in data:
        deal.take_profit_price = data["take_profit_price"]
    if "stop_loss_price" in data:
        deal.stop_loss_price = data["stop_loss_price"]

    deal.save()

    return response(
        message="Deal updated successfully",
        status_code=200,
    )


@api_view(["DELETE"])
def delete_deal(request, deal_id):
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        return response(
            message=f"Deal with id {deal_id} does not exist", status_code=404
        )

    deal.delete()

    return response(
        message="Deal deleted successfully",
        status_code=200,
    )
