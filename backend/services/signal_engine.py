class SignalEngine:

    @staticmethod
    def classify(token):

        score = token.get(
            "score",
            0
        )

        if score >= 1200:
            return "SUPERNOVA"

        if score >= 900:
            return "BREAKOUT"

        if score >= 700:
            return "PARABOLIC"

        if score >= 500:
            return "SNIPER"

        if score >= 250:
            return "BUY"

        return "WATCH"