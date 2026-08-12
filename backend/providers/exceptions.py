class ProviderError(Exception):
    """
    Base provider exception.
    """


class ProviderConfigurationError(
    ProviderError
):
    """
    Provider configuration is invalid.
    """


class ProviderRequestError(
    ProviderError
):
    """
    Provider HTTP request failed.
    """


class ProviderResponseError(
    ProviderError
):
    """
    Provider returned an invalid response.
    """