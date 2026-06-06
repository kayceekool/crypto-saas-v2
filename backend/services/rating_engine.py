class RatingEngine:

    @staticmethod
    def rate(score):

        if score >= 1200:
            return "AI SUPERNOVA"

        if score >= 900:
            return "GOD CANDLE"

        if score >= 700:
            return "PARABOLIC"

        if score >= 500:
            return "GEM"

        if score >= 250:
            return "GOOD"

        return "RISKY"