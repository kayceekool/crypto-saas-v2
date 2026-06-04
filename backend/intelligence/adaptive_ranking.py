from intelligence.pattern_ai import (
    PatternAI
)


class AdaptiveRanking:

    @staticmethod
    def boost(token):

        pattern = PatternAI.detect(
            token
        )

        if pattern == "BREAKOUT":
            token["score"] += 150

        elif pattern == "ACCUMULATION":
            token["score"] += 75

        return token