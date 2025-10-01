import json
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.snapshot import Snapshot
from core.models.account import Account
from core.models.strategy import Strategy
from core.helpers.response import response
from decimal import Decimal, InvalidOperation
from core.serializers.snapshot import SnapshotSerializer


@api_view(["POST"])
def create_snapshot(request):
    schema = {
        "broker_account_number": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "strategy_prefix": {
            "type": "string",
            "required": False,
            "maxlength": 50,
            "empty": False,
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
        account = Account.objects.get(
            broker_account_number=data["broker_account_number"]
        )
    except Account.DoesNotExist:
        return response(
            message=f"Account with broker_account_number {data['broker_account_number']} does not exist",
            status_code=404,
        )

    strategy = None
    if data.get("strategy_prefix"):
        try:
            strategy = Strategy.objects.get(prefix=data["strategy_prefix"])
        except Strategy.DoesNotExist:
            return response(
                message=f"Strategy with prefix {data['strategy_prefix']} does not exist",
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
    broker_account_number = request.GET.get("broker_account_number")
    strategy_prefix = request.GET.get("strategy_prefix")
    event = request.GET.get("event")

    snapshots = Snapshot.objects.all()

    if broker_account_number:
        snapshots = snapshots.filter(
            account__broker_account_number=broker_account_number
        )

    if strategy_prefix:
        snapshots = snapshots.filter(strategy__prefix=strategy_prefix)

    if event:
        snapshots = snapshots.filter(event__icontains=event)

    serializer = SnapshotSerializer(snapshots, many=True)
    snapshots_data = serializer.data

    return response(
        message="Snapshots retrieved successfully",
        data=snapshots_data,
        status_code=200,
    )


@api_view(["PUT"])
def update_snapshot(request, snapshot_id):
    schema = {
        "broker_account_number": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "strategy_prefix": {
            "type": "string",
            "required": False,
            "maxlength": 50,
            "empty": False,
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

    if "broker_account_number" in data:
        try:
            account = Account.objects.get(
                broker_account_number=data["broker_account_number"]
            )
            snapshot.account = account
        except Account.DoesNotExist:
            return response(
                message=f"Account with broker_account_number {data['broker_account_number']} does not exist",
                status_code=404,
            )

    if "strategy_prefix" in data:
        if data["strategy_prefix"] is None:
            snapshot.strategy = None
        else:
            try:
                strategy = Strategy.objects.get(prefix=data["strategy_prefix"])
                snapshot.strategy = strategy
            except Strategy.DoesNotExist:
                return response(
                    message=f"Strategy with prefix {data['strategy_prefix']} does not exist",
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
