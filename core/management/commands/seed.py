from django.core.management.base import BaseCommand
from .seeders.account_seeder import AccountSeeder
from .seeders.strategy_seeder import StrategySeeder


class Command(BaseCommand):
    help = "Seed initial data"

    def handle(self, *args, **options):
        AccountSeeder.run()
        StrategySeeder.run()
        self.stdout.write(self.style.SUCCESS("Successfully seeded initial data"))
