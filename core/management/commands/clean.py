from django.core.management.base import BaseCommand
from .helpers.db.db_destroy_deal import DbDestroyDeal
from .helpers.db.db_destroy_snapshot import DbDestroySnapshot
from .helpers.db.db_destroy_heartbeat import DbDestroyHeartbeat
from .helpers.db.db_destroy_account import DbDestroyAccount
from .helpers.db.db_destroy_strategy import DbDestroyStrategy


class Command(BaseCommand):
    help = "Clean all data from database tables"

    def handle(self, *args, **options):
        DbDestroyDeal.run()
        DbDestroySnapshot.run()
        DbDestroyHeartbeat.run()
        DbDestroyAccount.run()
        DbDestroyStrategy.run()
        self.stdout.write(
            self.style.SUCCESS("Successfully cleaned all database tables")
        )
