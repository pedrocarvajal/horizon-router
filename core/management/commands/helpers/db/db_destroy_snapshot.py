from django.db import connection
from core.models.snapshot import Snapshot


class DbDestroySnapshot:
    @staticmethod
    def run():
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'snapshots'"
                )
                if cursor.fetchone():
                    Snapshot.objects.all().delete()
        except Exception:
            pass
