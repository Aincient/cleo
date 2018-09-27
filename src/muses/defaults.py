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

# Name of the module in which the importer plugins are registered.
IMPORTER_PLUGIN_MODULE_NAME = 'muses_importer_plugin'

# Name of the module in which the importer plugins are registered.
EXPORTER_PLUGIN_MODULE_NAME = 'muses_exporter_plugin'

DEBUG = False

FAIL_ON_ERRORS_IN_IMPORTER_PLUGINS = True
FAIL_ON_MISSING_IMPORTER_PLUGINS = True

FAIL_ON_ERRORS_IN_EXPORTER_PLUGINS = True
FAIL_ON_MISSING_EXPORTER_PLUGINS = True

CONFIG = {}
