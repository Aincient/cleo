from .conf import get_setting

__all__ = (
    'CONFIG',
    'DEBUG',
    'EXPORTER_PLUGIN_MODULE_NAME',
    'FAIL_ON_ERRORS_IN_EXPORTER_PLUGINS',
    'FAIL_ON_ERRORS_IN_IMPORTER_PLUGINS',
    'FAIL_ON_MISSING_EXPORTER_PLUGINS',
    'FAIL_ON_MISSING_IMPORTER_PLUGINS',
    'IMPORTER_PLUGIN_MODULE_NAME',
)

# **************************************************************
# **************************************************************
# *************************** Core *****************************
# **************************************************************
# **************************************************************

IMPORTER_PLUGIN_MODULE_NAME = get_setting('IMPORTER_PLUGIN_MODULE_NAME')
EXPORTER_PLUGIN_MODULE_NAME = get_setting('EXPORTER_PLUGIN_MODULE_NAME')

CONFIG = get_setting('CONFIG')

DEBUG = get_setting('DEBUG')

FAIL_ON_ERRORS_IN_IMPORTER_PLUGINS = get_setting(
    'FAIL_ON_ERRORS_IN_IMPORTER_PLUGINS'
)
FAIL_ON_MISSING_IMPORTER_PLUGINS = get_setting(
    'FAIL_ON_MISSING_IMPORTER_PLUGINS'
)

FAIL_ON_ERRORS_IN_EXPORTER_PLUGINS = get_setting(
    'FAIL_ON_ERRORS_IN_EXPORTER_PLUGINS'
)
FAIL_ON_MISSING_EXPORTER_PLUGINS = get_setting(
    'FAIL_ON_MISSING_EXPORTER_PLUGINS'
)
