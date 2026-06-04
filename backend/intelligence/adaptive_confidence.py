from intelligence.strategy_stats import (
    StrategyStats
)


class AdaptiveConfidence:

    @staticmethod
    def adjust(confidence):

        wr = StrategyStats.win_rate()

        if wr > 70:
            confidence += 10

        elif wr < 40:
            confidence -= 10

        return max(
            5,
            min(confidence, 99)
        )