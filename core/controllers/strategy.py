import json
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.strategy import Strategy
from core.helpers.response import response
from core.serializers.strategy import StrategySerializer


@api_view(["POST"])
def create_strategy(request):
    schema = {
        "name": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "prefix": {
            "type": "string",
            "required": True,
            "maxlength": 50,
            "empty": False,
        },
        "symbol": {
            "type": "string",
            "required": True,
            "maxlength": 100,
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

    strategy = Strategy.objects.create(
        name=data["name"],
        prefix=data["prefix"],
        symbol=data["symbol"],
    )

    return response(
        message="Strategy created successfully",
        data={"id": strategy.id},
        status_code=201,
    )


@api_view(["GET"])
def search_strategies(request):
    name = request.GET.get("name")
    prefix = request.GET.get("prefix")
    symbol = request.GET.get("symbol")

    strategies = Strategy.objects.all()

    if name:
        strategies = strategies.filter(name__icontains=name)

    if prefix:
        strategies = strategies.filter(prefix__icontains=prefix)

    if symbol:
        strategies = strategies.filter(symbol__icontains=symbol)

    serializer = StrategySerializer(strategies, many=True)
    strategies_data = serializer.data

    return response(
        message="Strategies retrieved successfully",
        data=strategies_data,
        status_code=200,
    )


@api_view(["PUT"])
def update_strategy(request, strategy_id):
    schema = {
        "name": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "prefix": {
            "type": "string",
            "required": False,
            "maxlength": 50,
            "empty": False,
        },
        "symbol": {
            "type": "string",
            "required": False,
            "maxlength": 100,
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
        strategy = Strategy.objects.get(id=strategy_id)
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with id {strategy_id} does not exist", status_code=404
        )

    if "name" in data:
        strategy.name = data["name"]
    if "prefix" in data:
        strategy.prefix = data["prefix"]
    if "symbol" in data:
        strategy.symbol = data["symbol"]

    strategy.save()

    return response(
        message="Strategy updated successfully",
        status_code=200,
    )


@api_view(["DELETE"])
def delete_strategy(request, strategy_id):
    try:
        strategy = Strategy.objects.get(id=strategy_id)
    except Strategy.DoesNotExist:
        return response(
            message=f"Strategy with id {strategy_id} does not exist", status_code=404
        )

    strategy.delete()

    return response(
        message="Strategy deleted successfully",
        status_code=200,
    )
