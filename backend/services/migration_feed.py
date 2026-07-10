class MigrationFeed:

    migrations = []

    @classmethod
    def add(

        cls,

        token

    ):

        cls.migrations.insert(

            0,

            token

        )

        cls.migrations = cls.migrations[:100]