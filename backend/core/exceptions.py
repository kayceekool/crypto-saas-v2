class PlatformError(Exception):
    """
    Base exception for the platform.
    """


class ConfigurationError(PlatformError):
    """
    Configuration error.
    """


class ProviderError(PlatformError):
    """
    Provider operation error.
    """


class SchedulerError(PlatformError):
    """
    Scheduler operation error.
    """