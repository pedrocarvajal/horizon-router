from django.db import connection
from core.models.heartbeat import Heartbeat


class DbDestroyHeartbeat:
    @staticmethod
    def run():
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'heartbeats'"
                )
                if cursor.fetchone():
                    Heartbeat.objects.all().delete()
        except Exception:
            pass
