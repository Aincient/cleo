import os
import logging

import dateutil

# from django.core.management import call_command
from django.db import IntegrityError

import six

from .discover import autodiscover
from .exceptions import (
    DoesNotExist,
    ImporterError,
    ExporterError,
    ImporterDoesNotExist,
    ExporterDoesNotExist,
    ImproperlyConfigured,
    InvalidRegistryItemType
)

from .collection.models import Item, Image
from .cifar10_helpers import prepare_images_list_for_cifar10, write_batch
from .helpers import safe_text, save_as_pickle
from .settings import (
    DEBUG,
    FAIL_ON_ERRORS_IN_IMPORTER_PLUGINS,
    FAIL_ON_ERRORS_IN_EXPORTER_PLUGINS,
    FAIL_ON_MISSING_IMPORTER_PLUGINS,
    FAIL_ON_MISSING_EXPORTER_PLUGINS,
    CONFIG,
)

LOGGER = logging.getLogger(__name__)

__all__ = (
    'BaseExporter',
    'BaseImporter',
    'BaseRegistry',
    'ensure_autodiscover',
    'exporter_registry',
    'ExporterRegistry',
    'get_importer_config',
    'get_registered_exporter_plugins',
    'get_registered_exporter_plugins_uids',
    'get_registered_importer_plugins',
    'get_registered_importer_plugins_uids',
    'get_registered_plugin_uids',
    'get_registered_plugins',
    'importer_registry',
    'ImporterRegistry',
)


class BaseRegistry(object):
    """Base registry.

    Registry of plugins. It's essential, that class registered has the
    ``uid`` property.

    If ``fail_on_missing_plugin`` is set to True, an appropriate exception
    (``plugin_not_found_exception_cls``) is raised in cases if plugin could't
    be found in the registry.

    :property mixed type:
    :property bool fail_on_missing_plugin:
    :property fobi.exceptions.DoesNotExist plugin_not_found_exception_cls:
    :property str plugin_not_found_error_message:
    """

    type = None
    fail_on_missing_plugin = False
    plugin_not_found_exception_cls = DoesNotExist
    plugin_not_found_error_message = "Can't find plugin with uid `{0}` in " \
                                     "`{1}` registry."

    def __init__(self):
        """Constructor."""
        assert self.type
        self._registry = {}
        self._forced = []

    @property
    def registry(self):
        """Shortcut to self._registry."""
        return self._registry

    def items(self):
        """Shortcut to self._registry.items()."""
        return self._registry.items()

    def register(self, cls, force=False):
        """Registers the plugin in the registry.

        :param mixed cls:
        :param bool force:
        """
        if not issubclass(cls, self.type):
            raise InvalidRegistryItemType(
                "Invalid item type `{0}` for registry "
                "`{1}`".format(cls, self.__class__)
            )

        # If item has not been forced yet, add/replace its' value in the
        # registry.
        if force:

            if cls.uid not in self._forced:
                self._registry[cls.uid] = cls
                self._forced.append(cls.uid)
                return True
            else:
                return False

        else:

            if cls.uid in self._registry:
                return False
            else:
                self._registry[cls.uid] = cls
                return True

    def unregister(self, cls):
        """Un-register."""
        if not issubclass(cls, self.type):
            raise InvalidRegistryItemType(
                "Invalid item type `{0}` for registry "
                "`{1}`".format(cls, self.__class__)
            )

        # Only non-forced items are allowed to be unregistered.
        if cls.uid in self._registry and cls.uid not in self._forced:
            self._registry.pop(cls.uid)
            return True
        else:
            return False

    def get(self, uid, default=None):
        """Get the given entry from the registry.

        :param string uid:
        :param mixed default:
        :return mixed.
        """
        item = self._registry.get(uid, default)

        if not item:
            err_msg = self.plugin_not_found_error_message.format(
                uid, self.__class__
            )
            if self.fail_on_missing_plugin:
                LOGGER.error(err_msg)
                raise self.plugin_not_found_exception_cls(err_msg)
            else:
                LOGGER.debug(err_msg)

        return item


class BaseImporter(object):
    """Base importer plugin.

    :Properties:

        - `uid` (string): Plugin uid (obligatory). Example value: 'dummy',
            'wysiwyg', 'news'.
        - `name` (string): Plugin name (obligatory). Example value:
            'Dummy plugin', 'WYSIWYG', 'Latest news'.
    """

    uid = None
    name = None
    api_language = None

    def __init__(self, user=None, options=None):
        """Constructor.

        :param django.contrib.auth.models.User user: Plugin owner.
        """
        # Making sure all necessary properties are defined.
        try:
            assert self.uid
            assert self.name
            assert self.api_language
        except Exception as err:
            raise NotImplementedError(
                "You should define `uid` and `name` properties in "
                "your `{0}.{1}` class. {2}".format(
                    self.__class__.__module__,
                    self.__class__.__name__,
                    str(err)
                )
            )
        self.user = user
        self.options = options
        self.driver = None

        # Some initial values
        self.request = None
        self.config = get_importer_config(self.uid)
        self.setup()

    def setup(self):
        """Set up.
        
        :return: 
        """
        # TODO

    def teardown(self):
        """Tear down.

        :return:
        """
        # TODO

        # call_command('flush', verbosity=0, interactive=False,
        #              reset_sequences=False,
        #              allow_cascade=False,
        #              inhibit_post_migrate=False)

    def run(self):
        """Run.

        :return:
        """
        return self.do_import()

    def do_import(self):
        """Import.

        :return:
        """
        raise NotImplementedError(
            "You should implement the `do_import` method in "
            "your `{0}.{1}` class.".format(
                self.__class__.__module__,
                self.__class__.__name__
            )
        )

    def do_update(self, fields):
        """Update imported items.

        :return:
        """
        raise NotImplementedError(
            "You should implement the `do_update` method in "
            "your `{0}.{1}` class.".format(
                self.__class__.__module__,
                self.__class__.__name__
            )
        )

    def save_item(self, item_data):
        """Save (insert) Item with given data.

        :param item_data:
        :type item_data: dict
        :return: muses.collection.Item instance
        :rtype: muses.collection.Item
        """
        if 'accession_date' in item_data:
            if isinstance(item_data['accession_date'], six.string_types):
                try:
                    item_data['accession_date'] = dateutil.parser.parse(
                        item_data['accession_date']
                    )
                except Exception as err:
                    item_data.pop('accession_date')
        try:
            item = Item.objects.create(**item_data)
            return item
        except IntegrityError as err:
            pass

    def get_item(self, item_data):
        """Get item object from database by given data.

        :param item_data:
        :type item_data: dict
        :return: muses.collection.Item instance
        :rtype: muses.collection.Item
        """
        id_data = {
            'record_number': item_data['record_number'],
            'inventory_number': item_data['inventory_number'],
            'importer_uid': self.uid,
        }
        try:
            item = Item.objects.get(**id_data)
            return item
        except IntegrityError as err:
            item = Item.objects.filter(**id_data).first()
            return item
        except Item.DoesNotExist as err:
            pass

    def save_images(self, item, images_list):
        """Save images.

        :param item: Item to associate with.
        :param images_list: List of dicts.
        :type item: muses.collection.Item
        :type images_list: list
        :return: List of muses.collection.Image instances.
        :rtype: list
        """
        images = []
        for image_data in images_list:
            # image_data.update({'item': item})
            # Images are retrieved based on their api_url
            # and data is updated if necessary
            try:
                api = image_data.pop('api_url', None)
                image, created = Image.objects.update_or_create(api_url=api, defaults=image_data)
                item.images.add(image)
                images.append(image)
            except Exception as err:
                # Something isn't right here. An image shouldn't appear
                # twice. Still, it does. See if we should be adding
                # many-to-many relations here.
                # LOGGER.debug(image_data)
                # LOGGER.debug(err)
                pass

        return images


class BaseExporter(object):
    """Base exporter plugin.

    :Properties:

        - `uid` (string): Plugin uid (obligatory). Example value: 'dummy',
            'wysiwyg', 'news'.
        - `name` (string): Plugin name (obligatory). Example value:
            'Dummy plugin', 'WYSIWYG', 'Latest news'.
    """

    uid = None
    name = None
    categories = {}
    reversed_categories = {}
    dataset_dir = None
    data_filename = 'data_batch_1'
    test_filename = 'test_batch'

    def __init__(self, user=None):
        """Constructor.

        :param django.contrib.auth.models.User user: Plugin owner.
        """
        # Making sure all necessary properties are defined.
        try:
            assert self.uid
            assert self.name
        except Exception as err:
            raise NotImplementedError(
                "You should define `uid` and `name` properties in "
                "your `{0}.{1}` class. {2}".format(
                    self.__class__.__module__,
                    self.__class__.__name__,
                    str(err)
                )
            )
        self.user = user
        self.driver = None

        # Some initial values
        self.request = None
        self.config = get_importer_config(self.uid)
        self.setup()
        for k, v in self.categories.items():
            self.reversed_categories.update({v: k})

    def setup(self):
        """Set up.

        :return:
        """
        # TODO

    def teardown(self):
        """Tear down.

        :return:
        """
        # TODO

    def run(self):
        """Run.

        We pickle results and save them in pickle format in batches of
        10,000.00 per file.

        :return:
        """
        data = self.do_export()

        number_of_items = len(data)
        number_of_test_items = int(number_of_items / 5)
        number_of_data_items = number_of_items - number_of_test_items

        data_items = data[0:number_of_data_items]
        test_items = data[number_of_data_items:]

        write_batch(
            images_list=data_items,
            dest_filename=os.path.join(self.dataset_dir, self.data_filename),
            text_labels=self.categories
        )

        write_batch(
            images_list=test_items,
            dest_filename=os.path.join(self.dataset_dir, self.test_filename),
            text_labels=self.categories
        )

        return data

    def get_categories(self):
        """Get categories.

        :return:
        :rtype: dict
        """
        raise NotImplementedError(
            "You should implement the `get_categories` method in "
            "your `{0}.{1}` class.".format(
                self.__class__.__module__,
                self.__class__.__name__
            )
        )

    def do_export(self):
        """Import.

        :return:
        """
        raise NotImplementedError(
            "You should implement the `do_export` method in "
            "your `{0}.{1}` class.".format(
                self.__class__.__module__,
                self.__class__.__name__
            )
        )

    def get_data_length(self):
        """Get data length.

        :return:
        """
        items = self.do_export()
        return len(items)


class ImporterRegistry(BaseRegistry):
    """Importer registry."""

    type = (BaseImporter,)
    fail_on_missing_plugin = FAIL_ON_MISSING_IMPORTER_PLUGINS
    plugin_not_found_exception_cls = ImporterDoesNotExist


# Register form field plugins by calling importer_registry.register()
importer_registry = ImporterRegistry()


class ExporterRegistry(BaseRegistry):
    """Exporter registry."""

    type = (BaseExporter,)
    fail_on_missing_plugin = FAIL_ON_MISSING_EXPORTER_PLUGINS
    plugin_not_found_exception_cls = ExporterDoesNotExist


# Register form field plugins by calling exporter_registry.register()
exporter_registry = ExporterRegistry()


def get_importer_config(importer_uid):
    """Get importer config.

    :param importer_uid:
    :return:
    """
    return CONFIG['importers'].get(importer_uid, {})


def ensure_autodiscover():
    """Ensure that plugins are auto-discovered.

    The form callbacks registry is intentionally left out, since they will be
    auto-discovered in any case if other modules are discovered.
    """
    if not importer_registry._registry or not exporter_registry._registry:
        autodiscover()


def get_registered_plugins(registry, as_instances=False, sort_items=True):
    """Get registered plugins.

    Get a list of registered plugins in a form if tuple (plugin name, plugin
    description). If not yet auto-discovered, auto-discovers them.

    :param registry:
    :param bool as_instances:
    :param bool sort_items:
    :return list:
    """
    ensure_autodiscover()

    if as_instances:
        return registry._registry

    registered_plugins = []

    for uid, plugin in registry._registry.items():
        plugin_name = safe_text(plugin.name)
        registered_plugins.append((uid, plugin_name))

    if sort_items:
        registered_plugins.sort()

    return registered_plugins


def get_registered_plugin_uids(registry, flattern=True, sort_items=True):
    """Get a list of registered plugin uids as a list .

    If not yet auto-discovered, auto-discovers them.

    The `sort_items` is applied only if `flattern` is True.

    :param registry:
    :param bool flattern:
    :param bool sort_items:
    :return list:
    """
    ensure_autodiscover()

    registered_plugin_uids = registry._registry.keys()

    if flattern:
        registered_plugin_uids = list(registered_plugin_uids)
        if sort_items:
            registered_plugin_uids.sort()

    return registered_plugin_uids


def get_registered_importer_plugins():
    """Get registered importer plugins.

    Gets a list of registered plugins in a form of tuple (plugin name, plugin
    description). If not yet auto-discovered, auto-discovers them.

    :return list:
    """
    return get_registered_plugins(importer_registry)


def get_registered_importer_plugins_uids():
    """Get registered importer plugin UIDs.

    Gets a list of registered plugins in a form of tuple (plugin name, plugin
    description). If not yet auto-discovered, auto-discovers them.

    :return list:
    """
    return get_registered_plugin_uids(importer_registry)


def get_registered_exporter_plugins():
    """Get registered importer plugins.

    Gets a list of registered plugins in a form of tuple (plugin name, plugin
    description). If not yet auto-discovered, auto-discovers them.

    :return list:
    """
    return get_registered_plugins(exporter_registry)


def get_registered_exporter_plugins_uids():
    """Get registered importer plugin UIDs.

    Gets a list of registered plugins in a form of tuple (plugin name, plugin
    description). If not yet auto-discovered, auto-discovers them.

    :return list:
    """
    return get_registered_plugin_uids(exporter_registry)
