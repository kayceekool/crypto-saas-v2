class LiveAlertFeed:

    alerts = []

    @classmethod
    def push(

        cls,

        alert

    ):

        cls.alerts.insert(

            0,

            alert

        )

        cls.alerts = cls.alerts[:200]