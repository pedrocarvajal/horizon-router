from core.models.strategy import Strategy


class DbDestroyStrategy:
    @staticmethod
    def run():
        Strategy.objects.all().delete()
