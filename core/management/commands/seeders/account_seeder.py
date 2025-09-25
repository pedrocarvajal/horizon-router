from core.models.account import Account


class AccountSeeder:
    @staticmethod
    def run():
        Account.objects.get_or_create(name="Pedro")
