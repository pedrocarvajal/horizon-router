from django.db import connection
from core.models.strategy import Strategy


class DbDestroyStrategy:
    @staticmethod
    def run():
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'strategies'"
                )
                if cursor.fetchone():
                    Strategy.objects.all().delete()
        except Exception:
            pass
