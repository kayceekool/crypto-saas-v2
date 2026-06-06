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

            token["score"] += 250

            token["signal"] = (
                "BREAKOUT"
            )

        elif pattern == "ACCUMULATION":

            token["score"] += 100

            token["signal"] = (
                "ACCUMULATION"
            )

        return token