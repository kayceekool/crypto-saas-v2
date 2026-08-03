from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class HealthManager:

    components: dict[str, dict] = field(
        default_factory=dict
    )

    def set_status(
        self,
        name: str,
        status: str,
        detail: str = "",
    ) -> None:

        self.components[name] = {

            "status": status,

            "detail": detail,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

    def snapshot(self) -> dict:

        statuses = [
            item["status"]
            for item in
            self.components.values()
        ]

        overall = "healthy"

        if any(
            status == "down"
            for status in statuses
        ):

            overall = "unhealthy"

        elif any(
            status == "degraded"
            for status in statuses
        ):

            overall = "degraded"

        return {

            "status": overall,

            "components":
                self.components,
        }


health_manager = HealthManager()