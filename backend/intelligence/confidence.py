class ConfidenceEngine:

    def calculate(
        self,
        *,
        score: float,
        pattern: str,
        risk: str,
    ) -> float:

        confidence = 50.0

        if score >= 1000:

            confidence += 20

        elif score >= 750:

            confidence += 12

        elif score >= 500:

            confidence += 6

        if pattern == "BREAKOUT":

            confidence += 10

        elif pattern == "ACCUMULATION":

            confidence += 5

        if risk == "HIGH":

            confidence -= 20

        elif risk == "MEDIUM":

            confidence -= 10

        elif risk == "LOW":

            confidence += 5

        return max(
            5.0,
            min(
                confidence,
                99.0,
            ),
        )