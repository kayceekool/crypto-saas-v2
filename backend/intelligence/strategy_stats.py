class StrategyStats:

    wins = 0
    losses = 0

    @classmethod
    def win_rate(cls):

        total = cls.wins + cls.losses

        if total == 0:
            return 0

        return round(
            cls.wins / total * 100,
            2
        )