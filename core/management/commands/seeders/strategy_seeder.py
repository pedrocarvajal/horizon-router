from core.models.strategy import Strategy


class StrategySeeder:
    @staticmethod
    def run():
        symbols = ["xauusd", "eurusd", "sp500", "stoxx50e", "usdchf", "xtiusd"]

        for symbol in symbols:
            Strategy.objects.get_or_create(name="SRSniper", prefix="SRS", symbol=symbol)
