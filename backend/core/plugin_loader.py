from importlib import import_module

from backend.core.logging import (
    get_logger,
)


logger = get_logger(
    "plugin_loader"
)


class PluginLoader:

    def __init__(self):

        self.loaded = []


    def load_module(
        self,
        module_path: str,
    ) -> None:

        if module_path in self.loaded:

            return

        import_module(
            module_path
        )

        self.loaded.append(
            module_path
        )

        logger.info(
            "Loaded plugin module: %s",
            module_path,
        )


plugin_loader = PluginLoader()