__all__ = (
    'DoesNotExist',
    'ExporterDoesNotExist',
    'ExporterError',
    'ImporterDoesNotExist',
    'ImporterError',
    'ImproperlyConfigured',
    'InvalidRegistryItemType',
    'MusesBaseException',
)


class MusesBaseException(Exception):
    """Base exception."""


class ImproperlyConfigured(MusesBaseException):
    """Improperly configured.

    Exception raised when developer didn't configure/write the code properly.
    """


class InvalidRegistryItemType(ValueError, MusesBaseException):
    """Invalid registry item type.

    Raised when an attempt is made to register an item in the registry which
    does not have a proper type.
    """


class DoesNotExist(MusesBaseException):
    """Raised when something does not exist."""


class ImporterDoesNotExist(DoesNotExist):
    """Raised when no importer with given uid can be found."""


class ImporterError(MusesBaseException):
    """Base error for importer."""


class ExporterDoesNotExist(DoesNotExist):
    """Raised when no exporter with given uid can be found."""


class ExporterError(MusesBaseException):
    """Base error for exporter."""
