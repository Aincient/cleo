"""
Helpers module. This module can be safely imported from any
social_profile_scrapper (sub)module, since it never imports from any of the
social_profile_scrapper (sub)modules (except for the
`social_profile_scrapper.constants` and `social_profile_scrapper.exceptions`
modules).
"""
import glob
import json
import logging
import os
import shutil
import signal
import subprocess
import uuid

from django.conf import settings
from django.core.files.base import File
from django.templatetags.static import static
from django.utils.encoding import force_text
from django.utils.html import format_html_join
# from django.utils.translation import ugettext_lazy as _

from eximagination.utils import obtain_image

from nine.versions import DJANGO_GTE_1_8, DJANGO_GTE_1_10
import numpy as np

from six import text_type, PY3
from six.moves.cPickle import dumps as pickle_dumps

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

try:
    from PIL import Image
except ImportError:
    import Image

__all__ = (
    'admin_change_url',
    'clean_dict',
    'clone_file',
    'combine_dicts',
    'convert_image_to_ndarray',
    'delete_file',
    'empty_string',
    'ensure_unique_filename',
    'flatatt_inverse_quotes',
    'get_app_label_and_model_name',
    'get_model_name_for_object',
    'get_registered_models',
    'handle_uploaded_file',
    'iterable_to_dict',
    'lists_overlap',
    'map_field_name_to_label',
    'remove_image_from_drive',
    'safe_text',
    'save_photo',
    'two_dicts_to_string',
    'uniquify_sequence',
    'dump_json_to_file',
)

logger = logging.getLogger(__name__)

# DEBUG = not True

# *****************************************************************************
# *****************************************************************************
# ********************************** General **********************************
# *****************************************************************************
# *****************************************************************************


def safe_text(text):
    """Safe text (encode).

    :return str:
    """
    if PY3:
        return force_text(text, encoding='utf-8')
    else:
        return force_text(text, encoding='utf-8').encode('utf-8')


def lists_overlap(sub, main):
    """Check whether lists overlap."""
    for i in sub:
        if i in main:
            return True
    return False


def iterable_to_dict(items, key_attr_name):
    """Converts iterable of certain objects to dict.

    :param iterable items:
    :param string key_attr_name: Attribute to use as a dictionary key.
    :return dict:
    """
    items_dict = {}
    for item in items:
        items_dict.update({getattr(item, key_attr_name): item})
    return items_dict


def map_field_name_to_label(form):
    """Takes a form and creates label to field name map.

    :param django.forms.Form form: Instance of ``django.forms.Form``.
    :return dict:
    """
    return dict([(field_name, field.label)
                 for (field_name, field)
                 in form.base_fields.items()])


def clean_dict(source, keys=[], values=[]):
    """Removes given keys and values from dictionary.

    :param dict source:
    :param iterable keys:
    :param iterable values:
    :return dict:
    """
    dict_data = {}
    for key, value in source.items():
        if (key not in keys) and (value not in values):
            dict_data[key] = value
    return dict_data


def combine_dicts(headers, data):
    """Combine dicts.

    Takes two dictionaries, assuming one contains a mapping keys to titles
    and another keys to data. Joins as string and returns a result dict.
    """
    return [(value, data.get(key, '')) for key, value in list(headers.items())]


def two_dicts_to_string(headers, data, html_element='p'):
    """Two dicts to string.

    Takes two dictionaries, assuming one contains a mapping keys to titles
    and another keys to data. Joins as string and returns wrapped into
    HTML "p" tag.
    """
    formatted_data = [
        (value, data.get(key, '')) for key, value in list(headers.items())
    ]
    return "".join(
        ["<{0}>{1}: {2}</{3}>".format(html_element, safe_text(key),
                                      safe_text(value), html_element)
         for key, value in formatted_data]
    )


empty_string = text_type('')


def absolute_path(path):
    """
    Given a relative or absolute path to a static asset, return an absolute
    path. An absolute path will be returned unchanged while a relative path
    will be passed to django.templatetags.static.static().
    """
    if path.startswith(('http://', 'https://', '/')):
        return path
    return static(path)


def uniquify_sequence(sequence):
    """Uniqify sequence.

    Makes sure items in the given sequence are unique, having the original
    order preserved.

    :param iterable sequence:
    :return list:
    """
    seen = set()
    seen_add = seen.add
    return [absolute_path(x)
            for x in sequence if x not in seen and not seen_add(x)]


def get_ignorable_form_values():
    """Get ignorable for form values.

    Gets an iterable of form values to ignore.

    :return iterable:
    """
    return [None, empty_string]


def get_model_name_for_object(obj):
    """Get model name for object.

    Django version agnostic."""
    return obj._meta.model_name

# *****************************************************************************
# *****************************************************************************
# ****************************** File helpers *********************************
# *****************************************************************************
# *****************************************************************************


def ensure_unique_filename(destination):
    """Makes sure filenames are never overwritten.

    :param string destination:
    :return string:
    """
    if os.path.exists(destination):
        filename, extension = os.path.splitext(destination)
        return "{0}_{1}{2}".format(filename, uuid.uuid4(), extension)
    else:
        return destination


def handle_uploaded_file(upload_dir, image_file):
    """Handle uploaded files.

    :param django.core.files.uploadedfile.InMemoryUploadedFile image_file:
    :return string: Path to the image (relative).
    """
    upload_dir_absolute_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

    # Create path if doesn't exist yet
    if not os.path.exists(upload_dir_absolute_path):
        os.makedirs(upload_dir_absolute_path)

    if isinstance(image_file, File):
        destination_path = ensure_unique_filename(
            os.path.join(upload_dir_absolute_path, image_file.name)
        )
        image_filename = image_file.name
        with open(destination_path, 'wb+') as destination:
            image_filename = os.path.basename(destination.name)
            for chunk in image_file.chunks():
                destination.write(chunk)
        return os.path.join(upload_dir, image_filename)
    return image_file


def delete_file(image_file):
    """Delete file from disc."""
    try:
        # Delete the main file.
        file_path = os.path.join(settings.MEDIA_ROOT, image_file)
        os.remove(file_path)

        # Delete the sized version of it.
        files = glob.glob("{0}*".format(file_path))
        for __f in files:
            try:
                os.remove(__f)
            except Exception as err:
                logger.debug(str(err))

        # If all goes well...
        return True
    except Exception as err:
        logger.debug(str(err))
        return False


def clone_file(upload_dir, source_filename, relative_path=True):
    """
    Clones the file.

    :param string source_filename: Source filename.
    :return string: Filename of the cloned file.
    """
    if source_filename.startswith(upload_dir):
        source_filename = os.path.join(settings.MEDIA_ROOT, source_filename)

    destination_filename = ensure_unique_filename(source_filename)
    try:
        shutil.copyfile(source_filename, destination_filename)
        if relative_path:
            destination_filename = destination_filename.replace(
                settings.MEDIA_ROOT, ''
            )
            if destination_filename.startswith('/'):
                destination_filename = destination_filename[1:]
        return destination_filename
    except Exception as err:
        logger.debug(str(err))


def extract_file_path(name):
    """Extracts the file path.

    :param string name:
    :return string:
    """
    return os.path.join(settings.MEDIA_ROOT, name)

# *****************************************************************************
# *****************************************************************************
# ****************************** Model helpers ********************************
# *****************************************************************************
# *****************************************************************************


def get_registered_models(ignore=[]):
    """Gets registered models as list.

    :param iterable ignore: Ignore the following content types (should
        be in ``app_label.model`` format (example ``auth.User``).
    :return list:
    """
    get_models = django.apps.apps.get_models
    # if DJANGO_GTE_1_7:
    #     get_models = django.apps.apps.get_models
    # else:
    #     def get_models():
    #         """Get models."""
    #         return models.get_models(include_auto_created=True)

    registered_models = [
        (
            "{0}.{1}".format(_m._meta.app_label, _m._meta.model_name),
            _m._meta.object_name
        )
        for _m
        in get_models()
    ]

    # registered_models = []
    # try:
    #     content_types = ContentType._default_manager.all()
    #
    #     for content_type in content_types:
    #         # model = content_type.model_class()
    #         content_type_id = "{0}.{1}".format(
    #             content_type.app_label, content_type.model
    #         )
    #         if content_type_id not in ignore:
    #             registered_models.append(
    #                 (content_type_id, content_type.name)
    #             )
    # except DatabaseError as err:
    #     logger.debug(str(err))

    return registered_models


def get_app_label_and_model_name(path):
    """Gets app_label and model_name from the path given.

    :param str path: Dotted path to the model (without ".model", as stored
        in the Django `ContentType` model.
    :return tuple: app_label, model_name
    """
    parts = path.split('.')
    return ''.join(parts[:-1]), parts[-1]

# *****************************************************************************
# *****************************************************************************
# **************************** Scrapper helpers *******************************
# *****************************************************************************
# *****************************************************************************


def phantom_js_clean_up():
    """Clean up Phantom JS.

    Kills all phantomjs instances, disregard of their origin.
    """
    processes = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = processes.communicate()

    for line in out.splitlines():
        if 'phantomjs' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def save_photo(image_source, save_to, media_url):
    """Save collection image.

    :param image_source: Photo URL.
    :param save_to: Directory to save the image to.
    :param media_url:
    :type image_source: str
    :type save_to: str
    :type media_url:
    :return: List of strings - paths to saved images.
    """
    file_data = obtain_image(
        image_source=image_source,
        save_to=save_to,
        media_url=media_url,
        force_update=False,
        debug=settings.DEBUG
    )
    if file_data:
        image_path = file_data[0]
        if settings.MEDIA_URL in image_path:
            image_path = image_path.replace(settings.MEDIA_URL, '')
        return image_path

# *****************************************************************************
# *****************************************************************************
# ****************************** Admin helpers ********************************
# *****************************************************************************
# *****************************************************************************


def admin_change_url(app_label, module_name, object_id, extra_path='',
                     url_title=None):
    """
    Gets an admin change URL for the object given.

    :param str app_label:
    :param str module_name:
    :param int object_id:
    :param str extra_path:
    :param str url_title: If given, an HTML a tag is returned with `url_title`
        as the tag title. If left to None just the URL string is returned.
    :return str:
    """
    try:
        url = reverse('admin:{0}_{1}_change'.format(app_label, module_name),
                      args=[object_id]) + extra_path
        if url_title:
            return u'<a href="{0}">{1}</a>'.format(url, url_title)
        else:
            return url
    except Exception:
        return None


def remove_image_from_drive(image_path, extra_dirs=None):
    """Remove image from drive.

    :param image_path:
    :param extra_dirs:
    :return:
    """
    if os.path.exists(image_path):
        os.remove(image_path)

    if extra_dirs is not None:
        for extra_dir in extra_dirs:
            _image_path = os.path.join(
                extra_dir,
                os.path.basename(image_path)
            )
            if os.path.exists(_image_path):
                os.remove(_image_path)

# *****************************************************************************
# *****************************************************************************
# ******************************** Export related *****************************
# *****************************************************************************
# *****************************************************************************


def flatatt_inverse_quotes(attrs):
    """Convert a dictionary of attributes to a single string.

    The returned string will contain a leading space followed by key="value",
    XML-style pairs. In the case of a boolean value, the key will appear
    without a value. It is assumed that the keys do not need to be
    XML-escaped. If the passed dictionary is empty, then return an empty
    string.

    The result is passed through 'mark_safe' (by way of 'format_html_join').
    """
    key_value_attrs = []
    boolean_attrs = []
    for attr, value in attrs.items():
        if isinstance(value, bool):
            if value:
                boolean_attrs.append((attr,))
        else:
            key_value_attrs.append((attr, value))

    return (
        format_html_join("", " {}='{}'", sorted(key_value_attrs)) +
        format_html_join("", " {}", sorted(boolean_attrs))
    )


def convert_image_to_ndarray(filename):
    """Convert image to `numpy.ndarray`.

    :param filename:
    :type filename: str
    :return:
    :rtype numpy.ndarray:
    """
    img = Image.open(filename)
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_as_pickle(data, out_filename_prefix):
    """Save as pickle.

    :param data:
    :param out_filename_prefix:
    :type data: list
    :type out_filename_prefix: str
    :return:
    """
    with open(out_filename_prefix, 'wb') as handle:
        pickle_dumps(data, handle)


def dump_json_to_file(data, filename):
    """Dump JSON to file.

    :param data:
    :param filename:
    :return:
    """
    with open(filename, 'w') as tmp_file:
        json.dump(data, tmp_file, ensure_ascii=False)
