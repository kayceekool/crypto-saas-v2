from dataclasses import dataclass
from typing import Any


@dataclass
class ProviderRecord:

    name: str

    provider: Any

    enabled: bool = True

    priority: int = 100


class ProviderRegistry:

    def __init__(self):

        self._providers = {}


    def register(
        self,
        name: str,
        provider: Any,
        *,
        priority: int = 100,
        enabled: bool = True,
    ) -> None:

        key = name.strip().lower()

        if not key:

            raise ValueError(
                "Provider name cannot be empty."
            )

        self._providers[key] = (
            ProviderRecord(
                name=name,
                provider=provider,
                enabled=enabled,
                priority=priority,
            )
        )


    def get(
        self,
        name: str,
    ) -> Any | None:

        record = self._providers.get(
            name.strip().lower()
        )

        if record is None:
            return None

        if not record.enabled:
            return None

        return record.provider


    def snapshot(self) -> dict:

        ordered = sorted(
            self._providers.values(),
            key=lambda item:
                item.priority,
        )

        return {

            "providers": [

                {
                    "name": item.name,

                    "enabled":
                        item.enabled,

                    "priority":
                        item.priority,
                }

                for item in ordered
            ]
        }


provider_registry = ProviderRegistry()