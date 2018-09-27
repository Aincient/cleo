from django.conf import settings

from . import defaults

__all__ = ('get_setting',)


def get_setting(setting, override=None):
    """Get setting.

    Get a setting from `muses` conf module, falling back to
    the default.

    If override is not None, it will be used instead of the setting.

    :param setting: String with setting name
    :param override: Value to use when no setting is available. Defaults to
        None.
    :return: Setting value.
    """
    attr_name = 'MUSES_{0}'.format(setting)
    if hasattr(settings, attr_name):
        return getattr(settings, attr_name)
    else:
        if hasattr(defaults, setting):
            return getattr(defaults, setting)
        else:
            return override
