from core.models.snapshot import Snapshot


class DbDestroySnapshot:
    @staticmethod
    def run():
        Snapshot.objects.all().delete()
