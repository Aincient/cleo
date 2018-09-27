"""
It's important that:

- Original images are automatically resized to 960x960.
- Thumbnails have the same names, just located in a different directory.

That what we have the ``same_name_custom_dir`` for.
"""
import os
import uuid

import six

from django.conf import settings

from imagekit.utils import format_to_extension, suggest_extension

# IMAGEKIT_CACHEFILE_DIR = os.path.join(
#     settings.MEDIA_ROOT,
#     'collection_images_medium'
# )

__all__ = ('same_name_custom_dir',)


def same_name_custom_dir(generator):
    """
    A namer that, given the following source file name:

        collection_images/bulldog.jpg

    will generate a name like this:

        collection_images_medium/bulldog.jpg

    where "collection_images_medium" is the value specified by
    the ``IMAGEKIT_CACHEFILE_DIR`` setting.
    """
    source_filename = getattr(generator.source, 'name', None)
    suffix = generator.options.get('suffix', str(uuid.uuid4()))

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        _dir = settings.IMAGEKIT_CACHEFILE_DIR
        filename_without_extension = os.path.splitext(
            os.path.basename(source_filename)
        )[0]
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        filename_without_extension = os.path.splitext(
            os.path.basename(source_filename)
        )[0]

        if isinstance(filename_without_extension, six.binary_type):
            filename_without_extension = filename_without_extension.decode()

        _dir = settings.IMAGEKIT_CACHEFILE_DIR

    ext = suggest_extension(source_filename or '', generator.format)

    return os.path.normpath(
        os.path.join(
            _dir,
            '{}{}{}'.format(
                filename_without_extension,
                suffix,
                ext
            )
        )
    )
