from intelligence.strategy_stats import (
    StrategyStats
)


class PerformanceFeedback:

    @staticmethod
    def update(pnl):

        if pnl > 0:

            StrategyStats.wins += 1

        else:

            StrategyStats.losses += 1