from intelligence.launch_ai import (
    LaunchAI
)

from intelligence.migration_ai import (
    MigrationAI
)


class MasterAI:

    @staticmethod
    def enhance(token):

        token["score"] += (
            LaunchAI.score(token)
        )

        token["score"] += (
            MigrationAI.score(token)
        )

        return token