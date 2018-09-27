import logging
import sys

from django.utils.module_loading import autodiscover_modules

import six

from .conf import get_setting

logger = logging.getLogger(__file__)

__all__ = ('autodiscover',)


def autodiscover():
    """Auto-discovers files that should be found by fobi."""
    # For Python 3 we need to increase the recursion limit, otherwise things
    # break. What we want is to set the recursion limit back to its' initial
    # value after all plugins have been discovered.
    recursion_limit = 1500
    default_recursion_limit = sys.getrecursionlimit()

    if six.PY3 and recursion_limit > default_recursion_limit:
        sys.setrecursionlimit(recursion_limit)

    importer_plugin_module_name = get_setting(
        'IMPORTER_PLUGIN_MODULE_NAME'
    )

    exporter_plugin_module_name = get_setting(
        'EXPORTER_PLUGIN_MODULE_NAME'
    )

    # Discover modules
    autodiscover_modules(importer_plugin_module_name)
    autodiscover_modules(exporter_plugin_module_name)

    if six.PY3 and recursion_limit > default_recursion_limit:
        sys.setrecursionlimit(default_recursion_limit)
