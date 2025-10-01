import json
from rest_framework.decorators import api_view
from cerberus import Validator
from core.models.account import Account
from core.helpers.response import response
from core.serializers.account import AccountSerializer


@api_view(["POST"])
def create_account(request):
    schema = {
        "name": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "broker_account_number": {
            "type": "string",
            "required": True,
            "maxlength": 255,
            "empty": False,
        },
        "broker_name": {
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

    account = Account.objects.create(
        name=data["name"],
        broker_account_number=data["broker_account_number"],
        broker_name=data["broker_name"],
    )

    return response(
        message="Account created successfully",
        data={"id": account.id},
        status_code=201,
    )


@api_view(["GET"])
def search_accounts(request):
    name = request.GET.get("name")
    broker_name = request.GET.get("broker_name")
    broker_account_number = request.GET.get("broker_account_number")

    accounts = Account.objects.all()

    if name:
        accounts = accounts.filter(name__icontains=name)

    if broker_name:
        accounts = accounts.filter(broker_name__icontains=broker_name)

    if broker_account_number:
        accounts = accounts.filter(
            broker_account_number__icontains=broker_account_number
        )

    serializer = AccountSerializer(accounts, many=True)
    accounts_data = serializer.data

    return response(
        message="Accounts retrieved successfully",
        data=accounts_data,
        status_code=200,
    )


@api_view(["PUT"])
def update_account(request, account_id):
    schema = {
        "name": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "broker_account_number": {
            "type": "string",
            "required": False,
            "maxlength": 255,
            "empty": False,
        },
        "broker_name": {
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
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return response(
            message=f"Account with id {account_id} does not exist", status_code=404
        )

    if "name" in data:
        account.name = data["name"]
    if "broker_account_number" in data:
        account.broker_account_number = data["broker_account_number"]
    if "broker_name" in data:
        account.broker_name = data["broker_name"]

    account.save()

    return response(
        message="Account updated successfully",
        status_code=200,
    )


@api_view(["DELETE"])
def delete_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return response(
            message=f"Account with id {account_id} does not exist", status_code=404
        )

    account.delete()

    return response(
        message="Account deleted successfully",
        status_code=200,
    )
