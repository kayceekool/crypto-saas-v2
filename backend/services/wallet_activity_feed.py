class WalletActivityFeed:

    activity = []

    @classmethod
    def push(

        cls,

        event

    ):

        cls.activity.insert(

            0,

            event

        )

        cls.activity = cls.activity[:300]