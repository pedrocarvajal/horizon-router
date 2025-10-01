from core.models.strategy import Strategy


class DbSeedStrategy:
    @staticmethod
    def run():
        strategies = [
            {
                "name": "EURUSD.EHighBreakout",
                "prefix": "EURUSD.EHB",
                "symbol": "eurusd",
            },
            {"name": "EURUSD.SRSniper", "prefix": "EURUSD.SRS", "symbol": "eurusd"},
            {"name": "SP500.EHighBreakout", "prefix": "SP500.EHB", "symbol": "sp500"},
            {"name": "SP500.SRSniper", "prefix": "SP500.SRS", "symbol": "sp500"},
            {"name": "UK100.EHighBreakout", "prefix": "UK100.EHB", "symbol": "uk100"},
            {"name": "UK100.SRSniper", "prefix": "UK100.SRS", "symbol": "uk100"},
            {
                "name": "USDCHF.EHighBreakout",
                "prefix": "USDCHF.EHB",
                "symbol": "usdchf",
            },
            {"name": "USDCHF.SRSniper", "prefix": "USDCHF.SRS", "symbol": "usdchf"},
            {
                "name": "USDJPY.EHighBreakout",
                "prefix": "USDJPY.EHB",
                "symbol": "usdjpy",
            },
            {"name": "USDJPY.SRSniper", "prefix": "USDJPY.SRS", "symbol": "usdjpy"},
            {
                "name": "XAGUSD.EHighBreakout",
                "prefix": "XAGUSD.EHB",
                "symbol": "xagusd",
            },
            {"name": "XAGUSD.SRSniper", "prefix": "XAGUSD.SRS", "symbol": "xagusd"},
            {
                "name": "XAUUSD.EHighBreakout",
                "prefix": "XAUUSD.EHB",
                "symbol": "xauusd",
            },
            {"name": "XAUUSD.SRSniper", "prefix": "XAUUSD.SRS", "symbol": "xauusd"},
            {"name": "XAUUSD.Test", "prefix": "XAUUSD.TST", "symbol": "xauusd"},
            {
                "name": "XTIUSD.EHighBreakout",
                "prefix": "XTIUSD.EHB",
                "symbol": "xtiusd",
            },
            {"name": "XTIUSD.SRSniper", "prefix": "XTIUSD.SRS", "symbol": "xtiusd"},
        ]

        for strategy_data in strategies:
            Strategy.objects.get_or_create(
                name=strategy_data["name"],
                prefix=strategy_data["prefix"],
                symbol=strategy_data["symbol"],
            )
