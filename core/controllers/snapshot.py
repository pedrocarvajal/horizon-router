import json
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.snapshot import Snapshot
from core.models.account import Account
from core.models.strategy import Strategy
from core.helpers.response import response
from decimal import Decimal, InvalidOperation


@api_view(["POST"])
def create_snapshot(request):
    schema = {
        "account_id": {
            "type": "integer",
            "required": True,
        },
        "strategy_id": {
            "type": "integer",
            "required": False,
            "nullable": True,
        },
        "event": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "nav": {
            "type": "string",
            "required": True,
            "empty": False,
        },
        "exposure": {
            "type": "string",
            "required": True,
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
        account = Account.objects.get(id=data["account_id"])
    except Account.DoesNotExist:
        return response(
            message=f"Account with id {data['account_id']} does not exist",
            status_code=404,
        )

    strategy = None
    if data.get("strategy_id"):
        try:
            strategy = Strategy.objects.get(id=data["strategy_id"])
        except Strategy.DoesNotExist:
            return response(
                message=f"Strategy with id {data['strategy_id']} does not exist",
                status_code=404,
            )

    try:
        nav = Decimal(data["nav"])
        exposure = Decimal(data["exposure"])
    except InvalidOperation:
        return response(
            message="Invalid decimal format for nav or exposure", status_code=400
        )

    snapshot = Snapshot.objects.create(
        account=account,
        strategy=strategy,
        event=data["event"],
        nav=nav,
        exposure=exposure,
    )

    return response(
        message="Snapshot created successfully",
        data={"id": snapshot.id},
        status_code=201,
    )


@api_view(["GET"])
def search_snapshots(request):
    account_id = request.GET.get("account_id")
    strategy_id = request.GET.get("strategy_id")
    event = request.GET.get("event")

    snapshots = Snapshot.objects.all()

    if account_id:
        snapshots = snapshots.filter(account_id=account_id)

    if strategy_id:
        snapshots = snapshots.filter(strategy_id=strategy_id)

    if event:
        snapshots = snapshots.filter(event__icontains=event)

    snapshots_data = [
        {
            "id": snapshot.id,
            "account": {
                "id": snapshot.account.id,
                "name": snapshot.account.name,
            },
            "strategy": {
                "id": snapshot.strategy.id,
                "name": snapshot.strategy.name,
                "prefix": snapshot.strategy.prefix,
            }
            if snapshot.strategy
            else None,
            "event": snapshot.event,
            "nav": str(snapshot.nav),
            "exposure": str(snapshot.exposure),
            "created_at": snapshot.created_at.isoformat(),
            "updated_at": snapshot.updated_at.isoformat(),
        }
        for snapshot in snapshots
    ]

    return response(
        message="Snapshots retrieved successfully",
        data=snapshots_data,
        status_code=200,
    )


@api_view(["PUT"])
def update_snapshot(request, snapshot_id):
    schema = {
        "account_id": {
            "type": "integer",
            "required": False,
        },
        "strategy_id": {
            "type": "integer",
            "required": False,
            "nullable": True,
        },
        "event": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "nav": {
            "type": "string",
            "required": False,
            "empty": False,
        },
        "exposure": {
            "type": "string",
            "required": False,
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
        snapshot = Snapshot.objects.get(id=snapshot_id)
    except Snapshot.DoesNotExist:
        return response(
            message=f"Snapshot with id {snapshot_id} does not exist", status_code=404
        )

    if "account_id" in data:
        try:
            account = Account.objects.get(id=data["account_id"])
            snapshot.account = account
        except Account.DoesNotExist:
            return response(
                message=f"Account with id {data['account_id']} does not exist",
                status_code=404,
            )

    if "strategy_id" in data:
        if data["strategy_id"] is None:
            snapshot.strategy = None
        else:
            try:
                strategy = Strategy.objects.get(id=data["strategy_id"])
                snapshot.strategy = strategy
            except Strategy.DoesNotExist:
                return response(
                    message=f"Strategy with id {data['strategy_id']} does not exist",
                    status_code=404,
                )

    if "event" in data:
        snapshot.event = data["event"]

    if "nav" in data:
        try:
            snapshot.nav = Decimal(data["nav"])
        except InvalidOperation:
            return response(message="Invalid decimal format for nav", status_code=400)

    if "exposure" in data:
        try:
            snapshot.exposure = Decimal(data["exposure"])
        except InvalidOperation:
            return response(
                message="Invalid decimal format for exposure", status_code=400
            )

    snapshot.save()

    return response(
        message="Snapshot updated successfully",
        status_code=200,
    )


@api_view(["DELETE"])
def delete_snapshot(request, snapshot_id):
    try:
        snapshot = Snapshot.objects.get(id=snapshot_id)
    except Snapshot.DoesNotExist:
        return response(
            message=f"Snapshot with id {snapshot_id} does not exist", status_code=404
        )

    snapshot.delete()

    return response(
        message="Snapshot deleted successfully",
        status_code=200,
    )
