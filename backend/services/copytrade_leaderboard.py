class CopyTradeLeaderboard:

    traders = []

    @classmethod
    def update(

        cls,

        signal

    ):

        cls.traders.append(
            signal
        )

        cls.traders = sorted(

            cls.traders,

            key=lambda s:

            s.get(
                "confidence",
                0
            ),

            reverse=True

        )[:100]