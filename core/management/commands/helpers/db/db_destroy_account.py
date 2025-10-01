from django.db import connection
from core.models.account import Account


class DbDestroyAccount:
    @staticmethod
    def run():
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'accounts'"
                )
                if cursor.fetchone():
                    Account.objects.all().delete()
        except Exception:
            pass
