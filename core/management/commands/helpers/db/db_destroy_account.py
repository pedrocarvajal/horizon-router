from core.models.account import Account


class DbDestroyAccount:
    @staticmethod
    def run():
        Account.objects.all().delete()
