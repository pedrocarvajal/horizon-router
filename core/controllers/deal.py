import json
from datetime import datetime
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.deal import Deal
from core.models.strategy import Strategy
from core.models.account import Account
from core.helpers.response import response


@api_view(["POST"])
def create_deal(request):
    schema = {
        "token": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "strategy_id": {
            "type": "integer",
            "required": True,
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
            "type": "string",
            "required": True,
            "maxlength": 50,
            "empty": False,
        },
        "direction": {
            "type": "integer",
            "required": True,
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
        "account_id": {
            "type": "integer",
            "required": True,
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
        strategy = Strategy.objects.get(id=data["strategy_id"])
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with id {data['strategy_id']} does not exist",
            status_code=404,
        )

    try:
        account = Account.objects.get(id=data["account_id"])
    except Account.DoesNotExist:
        return response(
            message=f"Account with id {data['account_id']} does not exist",
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
        account=account,
    )

    return response(
        message="Deal created successfully",
        data={"id": deal.id},
        status_code=201,
    )


@api_view(["GET"])
def search_deals(request):
    token = request.GET.get("token")
    strategy_id = request.GET.get("strategy_id")
    symbol = request.GET.get("symbol")
    type_param = request.GET.get("type")
    direction = request.GET.get("direction")
    account_id = request.GET.get("account_id")

    deals = Deal.objects.select_related("strategy", "account").all()

    if token:
        deals = deals.filter(token__icontains=token)

    if strategy_id:
        deals = deals.filter(strategy_id=strategy_id)

    if symbol:
        deals = deals.filter(symbol__icontains=symbol)

    if type_param:
        deals = deals.filter(type__icontains=type_param)

    if direction:
        deals = deals.filter(direction=direction)

    if account_id:
        deals = deals.filter(account_id=account_id)

    deals_data = [
        {
            "id": deal.id,
            "token": deal.token,
            "strategy": {
                "id": deal.strategy.id,
                "name": deal.strategy.name,
                "prefix": deal.strategy.prefix,
            },
            "time": deal.time.isoformat(),
            "symbol": deal.symbol,
            "type": deal.type,
            "direction": deal.direction,
            "volume": str(deal.volume),
            "price": str(deal.price),
            "profit": str(deal.profit) if deal.profit is not None else None,
            "account": {
                "id": deal.account.id,
                "name": deal.account.name,
            },
            "created_at": deal.created_at.isoformat(),
            "updated_at": deal.updated_at.isoformat(),
        }
        for deal in deals
    ]

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
            "type": "string",
            "required": False,
            "maxlength": 50,
            "empty": False,
        },
        "direction": {
            "type": "integer",
            "required": False,
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
        "account_id": {
            "type": "integer",
            "required": False,
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

    if "account_id" in data:
        try:
            account = Account.objects.get(id=data["account_id"])
            deal.account = account
        except Account.DoesNotExist:
            return response(
                message=f"Account with id {data['account_id']} does not exist",
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
