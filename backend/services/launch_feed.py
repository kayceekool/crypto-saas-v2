class LaunchFeed:

    launches = []

    @classmethod
    def add(

        cls,

        token

    ):

        cls.launches.insert(

            0,

            token

        )

        cls.launches = cls.launches[:100]