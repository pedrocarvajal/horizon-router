from core.models.deal import Deal


class DbDestroyDeal:
    @staticmethod
    def run():
        Deal.objects.all().delete()
