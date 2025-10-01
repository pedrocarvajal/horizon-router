from core.models.account import Account


class DbSeedAccount:
    @staticmethod
    def run():
        Account.objects.get_or_create(
            name="Pedro",
            broker_account_number="3000085718",
            broker_name="Darwinex",
        )
