from core.models.heartbeat import Heartbeat


class DbDestroyHeartbeat:
    @staticmethod
    def run():
        Heartbeat.objects.all().delete()
