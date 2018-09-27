from .base import get_registered_exporter_plugins_uids, exporter_registry
from .exceptions import ExporterDoesNotExist

__all__ = (
    'do_export',
)


def do_export(exporter_uid=None):
    """Export data.

    :param exporter_uid:
    :type exporter_uid: str
    :return:
    """
    counter = 0
    exporter_plugins_uids = get_registered_exporter_plugins_uids()
    if exporter_uid:
        if exporter_uid in exporter_plugins_uids:
            exporter_cls = exporter_registry.get(exporter_uid)
            exporter = exporter_cls()
            number_of_items = len(exporter.run())
            if number_of_items:
                counter += number_of_items
            exporter.teardown()
        else:
            raise ExporterDoesNotExist("{} does not exist".format(
                exporter_uid)
            )
    else:
        for exporter_uid in exporter_plugins_uids:
            exporter_cls = exporter_registry.get(exporter_uid)
            exporter = exporter_cls()
            number_of_items = len(exporter.run())
            if number_of_items:
                counter += number_of_items
            exporter.teardown()
    return counter
