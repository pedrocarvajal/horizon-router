from django.core.management.base import BaseCommand
from .helpers.db.db_seed_account import DbSeedAccount
from .helpers.db.db_seed_strategy import DbSeedStrategy


class Command(BaseCommand):
    help = "Seed initial data"

    def handle(self, *args, **options):
        DbSeedAccount.run()
        DbSeedStrategy.run()
        self.stdout.write(self.style.SUCCESS("Successfully seeded initial data"))
