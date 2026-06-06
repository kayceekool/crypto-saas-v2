from intelligence.launch_ai import (
    LaunchAI
)

from intelligence.migration_ai import (
    MigrationAI
)

from services.signal_engine import (
    SignalEngine
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

        token["signal"] = (
            SignalEngine.classify(
                token
            )
        )

        return token