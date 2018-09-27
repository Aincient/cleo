import logging
import math
import json
import re
import os

from django.conf import settings
from django.db.models import Q

from eximagination.utils import obtain_image
from googleapiclient.discovery import build
import googlemaps
from memoize import memoize
from html import unescape

import six

from muses.cached_api_calls.constants import (
    DEFAULT_LATITUDE,
    DEFAULT_LONGITUDE,
    DEFAULT_GEO_LOCATION,
)
from muses.cached_api_calls.models import GeoCoding, Translation, ThesauriTranslation

from .conf import (
    COLLECTION_IMAGES_BASE_PATH,
    COLLECTION_IMAGES_BASE_URL,
    PLEIADES_PATH
)
from .constants import DEFAULT_TRANSLATED_FIELDS
from .models import Item, Period, Image as ItemImage
from .models.constants import PERIOD_MAPPING, THEBES_COORDINATES, MISSING_COUNTRIES

try:
    from PIL import Image, ImageChops
except ImportError:
    import Image, ImageChops

try:
    GOOGLE_TRANSLATE_SERVICE = build(
        'translate',
        'v2',
        developerKey=settings.GOOGLE_API_KEY
    )
except Exception as err:
    GOOGLE_TRANSLATE_SERVICE = None

try:
    GOOGLE_MAPS_SERVICE = googlemaps.Client(key=settings.GOOGLE_API_KEY)
except Exception as err:
    GOOGLE_MAPS_SERVICE = None

__all__ = (
    'clean_met_images',
    'get_geo_location',
    'make_images_active_and_download_files',
    'prepare_point_field_data',
    'save_collection_image',
    'translate',
    'translate_collection_items',
    'translate_many',
)

LOGGER = logging.getLogger(__name__)

with open(PLEIADES_PATH) as input_file:
    PLEIADES = json.load(input_file)

# TODO: currently, this requires you to manually add the 404 image to your
# media folder it would be better to store it somewhere else
try:
    im_404 = Image.open(os.path.join(settings.MEDIA_ROOT, '404.png'))
except Exception:
    im_404 = None


def save_collection_image(image,
                          destination_directory,
                          media_url,
                          obtain_image_func=obtain_image):
    """Save collection image.

    :param image: collection.Image object
    :param destination_directory: Directory to save the image to.
    :param media_url:
    :param obtain_image_func:
    :type image: collection.Image
    :type destination_directory: str
    :type media_url:
    :type obtain_image_func: Callable.
    :return: List of strings - paths to saved images.
    """
    file_data = obtain_image_func(
        image_source=image.api_url,
        save_to=destination_directory,
        media_url=media_url,
        force_update=False,
        debug=settings.DEBUG
    )
    if file_data:
        image_path = file_data[0]
        if settings.MEDIA_URL in image_path:
            image_path = image_path.replace(settings.MEDIA_URL, '')
        return image_path


def make_images_active_and_download_files(queryset=None,
                                          request=None,
                                          obtain_image_func=obtain_image):
    """Make images active and download files.

    :param queryset:
    :param request:
    :param obtain_image_func:
    :rtype: int
    :return: Number of items downloaded.
    """
    counter = 0
    images_list = []

    if queryset is None:
        queryset = ItemImage.objects.exclude(
            Q(api_url__isnull=True) | Q(api_url__exact='')
        ).filter(
            Q(image__isnull=False) | Q(image__exact=''),
        )

    for image in queryset:
        try:
            new_image_path = save_collection_image(
                image,
                COLLECTION_IMAGES_BASE_PATH,
                COLLECTION_IMAGES_BASE_URL,
                obtain_image_func=obtain_image_func
            )
            image.active = True
            image.image = new_image_path
            image.save()
            counter += 1
            images_list.append(image.image_sized.path)
        except Exception as err_:
            LOGGER.debug(err_)
    return counter


@memoize(timeout=60*10)   # Timeout shall be given in seconds
def build_thesauri_translations_table(source_language, target_language):
    """

    :return:
    """
    translations = ThesauriTranslation.objects.filter(
        source_language=source_language, target_language=target_language, disregard=False)
    values = list(translations.values())

    return values


def translate(text,
              source_language,
              target_language,
              use_cache=False,):
    """Translate the given text.

    The text is first pre-processed by translating all the concepts that can be found in Thesauri.
    Then the pre-processed text is translated with Google Translate.

    :param text: Original text.
    :param source_language: Translate from language.
    :param target_language: Translate to language.
    :param use_cache:
    :type text: str
    :type source_language: str
    :type target_language: str
    :type use_cache: bool
    :return: Translated text.
    :rtype: str
    """
    if not text:
        return text

    preprocessed_text = text

    values = build_thesauri_translations_table(
        source_language=source_language,
        target_language=target_language
    )

    words_in_text = [
        concept
        for concept
        in values
        if (
            re.search(r"\b" + re.escape(concept['original']) + r"\b", text, flags=re.I)
            and concept['translation_exists']
        )
    ]

    word_lengths = [len(x['original'].split(" ")) for x in words_in_text]
    ordered = [x for _, x in sorted(zip(word_lengths, words_in_text), key=lambda q: q[0], reverse=True)]
    for item in ordered:
        # Because we want to keep the casing the same in the original and translated text
        # We have to run this operation thrice, once for capitalized words and once for lowercase words
        # We put ~ around the pre-translated words to flag that they should not be translated again
        preprocessed_text = re.sub(r"\b" + re.escape(item['original']).capitalize() + r"\b",
                                   '~{}~'.format(item['translation'].capitalize()), preprocessed_text)
        preprocessed_text = re.sub(r"\b(?!~)" + re.escape(item['original']) + r"(?!~)\b",
                                   '~{}~'.format(item['translation']), preprocessed_text, flags=re.I)

    if use_cache:
        try:
            translation = Translation.objects.get(
                original=preprocessed_text,
                source_language=source_language,
                target_language=target_language
            )
            return translation.translation
        except Translation.DoesNotExist:
            pass
        except Translation.MultipleObjectsReturned:
            # If multiple objects returned, fetch the first one
            translation = Translation.objects.filter(
                original=preprocessed_text,
                source_language=source_language,
                target_language=target_language
            ).first()
            return translation.translation

    if GOOGLE_TRANSLATE_SERVICE is None:
        return text

    res = GOOGLE_TRANSLATE_SERVICE.translations().list(
        source=source_language,
        target=target_language,
        q=[preprocessed_text]
    ).execute()

    try:
        # Using unescape because Google Translate API does not play nice with html characters
        translation = unescape(res['translations'][0]['translatedText'])
        translation = re.sub(' ~|~ |~', '', translation)
        LOGGER.debug(translation)
        if use_cache:
            Translation.objects.create(
                original=preprocessed_text,
                translation=translation,
                source_language=source_language,
                target_language=target_language
            )
        return translation
    except (KeyError, IndexError, TypeError) as err:
        return text


def translate_many(texts,
                   source_language,
                   target_language,
                   cache_results=False,
                   update_existing=False):
    """Translate many.

    :param texts:
    :param source_language:
    :param target_language:
    :param cache_results:
    :param update_existing:
    :return:
    :rtype: list
    """
    if GOOGLE_TRANSLATE_SERVICE is None:
        return texts

    res = GOOGLE_TRANSLATE_SERVICE.translations().list(
        source=source_language,
        target=target_language,
        q=texts
    ).execute()

    if res and 'translations' in res:
        return [r['translatedText'] for r in res['translations']]


def translate_collection_items(target_language,
                               translated_fields=DEFAULT_TRANSLATED_FIELDS,
                               items=None,
                               use_cache=False,
                               update_existing=False):
    """Translate collection items.

    :param target_language:
    :param translated_fields:
    :param items: QuerySet of :obj:`muses.collection.models.Item` objects.
    :param use_cache:
    :param update_existing:
    :type target_language: str
    :type translated_fields: tuple
    :type items: :obj:`django.db.models.query.QuerySet`.
    :type use_cache: bool
    :type update_existing: bool
    :return:
    """
    if not translated_fields:
        translated_fields = DEFAULT_TRANSLATED_FIELDS

    filters = []
    if not update_existing:
        for field in ['title']:
            filters.append(
                Q(**{"{}_{}__isnull".format(field, target_language): True})
                | Q(**{"{}_{}__exact".format(field, target_language): ''})
            )
    if not items:
        items = Item \
            .objects \
            .filter(*filters) \
            .exclude(language_code_orig=target_language)
    for item in items:
        for field in translated_fields:
            field_value = getattr(item, "{}_orig".format(field))

            # Skip on pure URLs
            if isinstance(field_value, six.string_types) \
                    and field_value.startswith('http'):
                continue

            translation = translate(
                text=field_value,
                source_language=item.language_code_orig,
                target_language=target_language,
                use_cache=use_cache,
            )
            setattr(item, "{}_{}".format(field, target_language), translation)
        item.save()


@memoize(timeout=60*10)  # Timeout shall be given in seconds
def get_pleiades_names(location):
    names = [n['romanized'].lower() for n in location['names']]
    names.append(location['title'].lower())
    return names


def get_geo_pleiades(name):
    """Get geo location from pleiades.

    :param name: name of the location
    :type name: str
    :return:
    :rtype:
    """
    if name.lower() in THEBES_COORDINATES:
        lat, lng = THEBES_COORDINATES[name.lower()]
        geo_location = "POINT ({} {})".format(
            lat,
            lng
        )
        return geo_location

    for location in PLEIADES:
        names = get_pleiades_names(location)
        if name.lower() in names:
            lng, lat = location['reprPoint']
            if lng and lat:
                geo_location = "POINT ({} {})".format(
                    lat,
                    lng
                )
                return geo_location


def prepare_point_field_data(res):
    """Prepare point field data.

    :param res:
    :return:
    """
    lat_lon = res[0]['geometry']['location']
    geo_location = "POINT ({} {})".format(
        lat_lon['lat'],
        lat_lon['lng']
    )
    return geo_location


def get_geo_location(name, use_cache=False):
    """Get geo location.

    :param name:
    :param use_cache:
    :type name: str
    :type use_cache: bool
    :return:
    :rtype:
    """
    res = None
    if not name:
        return name

    if use_cache:
        try:
            res = GeoCoding.objects.get(name=name)
            return res.geo_location
        except GeoCoding.DoesNotExist as err:
            pass

    if not GOOGLE_MAPS_SERVICE:
        return name

    # Before finding a location with Google maps, try to retrieve it from Pleiades
    # We first have to get the city name, because name is formatted as city, country

    newname = re.sub(";", ",", name)
    city_names = newname.split(',')[:-1]
    for city_name in city_names[::-1]:
        res = get_geo_pleiades(city_name)
        if res:
            break
    if res:
        if use_cache:
            GeoCoding.objects.get_or_create(
                name=name,
                geo_location=res
            )
        return res

    try:
        res = GOOGLE_MAPS_SERVICE.geocode(name)
    except googlemaps.exceptions.HTTPError as err:
        return DEFAULT_GEO_LOCATION

    try:
        geo_location = prepare_point_field_data(res)
        if use_cache:
            GeoCoding.objects.get_or_create(
                name=name,
                raw_response=res,
                geo_location=geo_location
            )
        return geo_location
    except (KeyError, IndexError, TypeError) as err:
        return DEFAULT_GEO_LOCATION


def fetch_geo_coordinates_collection_items(items=None,
                                           use_cache=False,
                                           update_existing=False):
    """Fetch geo coordinates for given collection items.

    :param items: QuerySet of :obj:`muses.collection.models.Item` objects.
    :param use_cache:
    :param update_existing:
    :type items: :obj:`django.db.models.query.QuerySet`.
    :type use_cache: bool
    :type update_existing: bool
    :return:
    """
    if not items:
        items = Item \
            .objects \
            .all() \
            .exclude(Q(country_en__isnull=True) | Q(country_en__iexact=''))

        if not update_existing:
            items = items.filter(
                Q(geo_location__isnull=True) | Q(geo_location__iexact='')
            )

    for item in items:
        # We have "city, country" string if city is available. Otherwise just
        # "country".
        location_str = ""
        if item.sub_region_en:
            location_str = "{}, ".format(item.sub_region_en)
        location_str = "{}{}, {}".format(location_str, item.city_en, item.country_en) \
            if item.city_en \
            else "{}{}".format(location_str, item.country_en)

        geo_location = get_geo_location(
            name=location_str,
            use_cache=use_cache
        )
        if geo_location:
            item.geo_location = geo_location
            item.save()


def get_period(item):
    """Get the period object that relates to the period of a collection item.

    :param item: The item object you want to find a node for
    :type item: Item
    :return:
    :rtype: Period
    """
    missing_periods = list()
    missing_dates = list()
    if item.period_en:
        period_names = item.period_en.split('; ')[::-1]
        if item.reign_en:
            reign = item.reign_en.split('; ')[::-1]
            period_names = reign + period_names

        for period_name in period_names:

            node = get_period_from_string(period_name)
            if node:
                return node

            # Split period name further on different separators
            for separator in [', ', '-', ' - ', ' or ', ' and ', ' to ', ' / ']:
                if separator in period_name:
                    for period_name_split in period_name.split(separator)[::-1]:
                        node = get_period_from_string(period_name_split)
                        if node:
                            return node

        if item.period_en not in missing_periods:
            missing_period_msg = 'No period can be found for period {} of item {}'.format(item.period_en, item.title_en)
            LOGGER.info(missing_period_msg)
            missing_periods.append(item.period_en)

    if item.object_date_begin_en and item.object_date_end_en:
        node = get_period_from_dates(item)
        if node:
            return node
        if (item.object_date_begin_en, item.object_date_end_en) not in missing_dates:
            missing_dates_msg = 'No period can be found for period between {} and {} of item {}'.format(
                item.object_date_begin_en, item.object_date_end_en, item.title_en)
            LOGGER.info(missing_dates_msg)
            missing_dates.append((item.object_date_begin_en, item.object_date_end_en))

    if not item.period_en and not (item.object_date_begin_en and item.object_date_end_en):
        missing_dating_msg = 'No dating information found for item {}'.format(item.title_en)
        LOGGER.info(missing_dating_msg)


def get_period_from_string(period_name):
    """Get the period node that matches a certain string

    :param period_name: The name of the period node you want to find
    :type period_name: str
    :return:
    :rtype: Period
    """
    if convert_roman_numerals(period_name.split(' ', 1)[0]):
        arabic_numeral = convert_roman_numerals(period_name.split(' ', 1)[0])
        period_name = period_name.replace(period_name.split(' ', 1)[0], arabic_numeral)

    # Remove unwanted patterns of characters, like "(?)"
    period_name = re.sub(" \(.*\)|\?| [0-9]* ?(AD|BC)?-[0-9]* ?(AD|BC)?\.?", "", period_name)
    period_name = re.sub("reigns? of ", "", period_name, flags=re.I)
    if period_name.lower() in PERIOD_MAPPING:
        period_name = PERIOD_MAPPING[period_name.lower()]
    try:
        period = Period.objects.get(
            name_en__iexact=period_name,
        )
        return period
    except Period.DoesNotExist:
        # If the period name starts with "early"  or "late", we'll strip the first word and
        # try to see if the new period name matches any node
        if period_name.lower().startswith("early ") or period_name.lower().startswith("late "):
            stripped = period_name.split(' ', 1)[1]
            return get_period_from_string(stripped)
        elif 'period' not in period_name.lower():
            period_name_period = period_name + ' period'
            return get_period_from_string(period_name_period)
        else:
            period_name = re.sub(' period', '', period_name)
            try:
                period = Period.objects.get(
                    name_en__startswith=period_name,
                )
                return period
            except Exception:
                return None


@memoize(timeout=60*10)  # Timeout shall be given in seconds
def get_leaf_nodes():
    """Get all the leaf nodes from the period tree

    :return:
    :rtype: list
    """
    leaf_nodes = [period for period in Period.objects.all() if period.is_leaf_node()]

    return leaf_nodes


def get_period_from_dates(item):
    """Get the period object that relates to the date range of a collection item.

    :param item:
    :type item: Item
    :return:
    :rtype: Period
    """
    # Sometimes both the start and end date are 0. In that case, we want to return None.
    if int(item.object_date_begin_en) == int(item.object_date_end_en) == 0:
        return None
    leaf_nodes = get_leaf_nodes()
    return get_period_from_nodes(item, leaf_nodes)


def get_period_from_nodes(item, node_list):
    """Return a period that matches the dates of an item from a list of periods
    Recursively iterates over parent nodes of current list

    :param item:
    :param node_list:
    :type item: Item
    :type node_list: list
    :return:
    :rtype: Period
    """
    parents = []
    for node in node_list:
        if node.date_begin_en and node.date_end_en:
            if int(node.date_begin_en) < int(item.object_date_begin_en) and \
                    int(item.object_date_end_en) < int(node.date_end_en):
                return node
        if node.parent:
            parents.append(node.parent)
    parents = list(set(parents))
    if parents:
        return get_period_from_nodes(item, parents)


def find_period_collection_items(items=None, update_existing=False):
    """Change period names for items to period names from Thesauri


    :param items: QuerySet of :obj:`muses.collection.models.Item` objects.
    :param update_existing:
    :type items: :obj:`django.db.models.query.QuerySet`.
    :type update_existing: bool
    :return:
    """
    filters = []
    if not update_existing:
        filters.append(
            Q(**{"{}__isnull".format('period_en'): True})
            | Q(**{"{}__exact".format('period_en'): ''})
        )

    if not items:
        items = Item \
            .objects \
            .filter(*filters)

    for item in items:
        period = get_period(item)
        if period:
            item.period_node = period
            item.save()


def roman_to_arabic(roman):
    """Convert Roman numerals to Arabic numerals

    :param roman:
    :type roman: str
    :return:
    :rtype: int
    """
    roman = roman.upper()
    invalid = ['IIII', 'VV', 'XXXX', 'LL', 'CCCC', 'DD', 'MMMM']
    if any(sub in roman for sub in invalid):
        return None
    to_arabic = {'IV': '4', 'IX': '9', 'XL': '40', 'XC': '90', 'CD': '400', 'CM': '900',
                 'I': '1', 'V': '5', 'X': '10', 'L': '50', 'C': '100', 'D': '500', 'M': '1000'}
    for key in to_arabic:
        if key in roman:
            roman = roman.replace(key, ' {}'.format(to_arabic.get(key)))
    try:
        arabic = sum(int(num) for num in roman.split())
        return arabic
    except ValueError:
        return None


def convert_roman_numerals(number):
    """Convert a Roman number to its Arabic ordinal counterpart

    :param number: A Roman number
    :type number: str
    :return:
    :rtype: str
    """
    arabic = roman_to_arabic(number)
    if arabic:
        ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])
        return ordinal(arabic)


def clean_field_names(items, field_names):
    """Remove redundant characters from item fields
    Currently removes (?), ? and any other variants
    Example:

    >>> items = Item.objects.all()
    >>> field_names = ['city_en', 'city_nl']
    >>> clean_field_names(items, field_names)

    :param items:  QuerySet of :obj:`muses.collection.models.Item` objects.
    :param field_names: list of field names that need to be cleaned
    :type items: :obj:`django.db.models.query.QuerySet`.
    :type field_names: list
    :return:
    """
    for item in items:
        for field in field_names:
            try:
                field_value = getattr(item, field)
                if field_value:
                    clean = re.sub(" ?\(?\?\)?| \( ?\)", "", field_value)
                    setattr(item, field, clean)
                    item.save()
            except AttributeError:
                print('Object has no attribute {}'.format(field))


def trim(im):
    """Trim black borders from an image

    :param im:
    :type im: Image
    :return:
    """
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def clean_met_images(queryset=None):
    """Remove black borders from MET images
    and set them to inactive if they are 404 screens.
    Only do this for images that are not yet trimmed.

    :param queryset:
    :return:
    """

    if queryset is None:
        queryset = ItemImage.objects.exclude(
            Q(image__isnull=True) | Q(image__exact='') |
            Q(trimmed=True),
        ).filter(
            Q(item__importer_uid='metmuseum_org') & Q(active=True)
        )

    for image in queryset:
        try:
            im = Image.open(image.image_large.path)
            im_trim = trim(im)
            if im == im_404:
                image.active = False
                image.trimmed = True
                image.save()
            else:
                im_trim.save(image.image_large.path)
                image.trimmed = True
                image.save()
        except Exception as err_:
            LOGGER.debug(err_)


def find_missing_countries(queryset=None):
    """Check if cities with missing countries are in the missing_countries list
    If so, add the right city to the item

    :param queryset: set of items
    :return:
    """
    if queryset is None:
        queryset = Item.objects.exclude(
            Q(city_en__isnull=True) | Q(city_en__exact=''),
        ).filter(
            Q(country_en__isnull=True) | Q(country_en__exact=''),
        )
    for item in queryset:
        try:
            if item.city_en.lower().strip() in MISSING_COUNTRIES:
                item.country_en = MISSING_COUNTRIES[item.city_en.lower().strip()]
                country_nl = translate(item.country_en, 'en', 'nl')
                item.country_nl = country_nl
                item.save()
        except Exception as err_:
            LOGGER.debug(err_)
    pass


def remove_item_list(inventory_numbers, dry_run=True, queryset=None):
    """Remove items with known inventory numbers

    :param inventory_numbers: list of inventory numbers to remove
    :param dry_run: set to True for testing
    :param queryset: optional queryset to remove them from
    :return:
    """
    if queryset is None:
        queryset = Item.objects.all()
    remove = queryset.filter(inventory_number__in=inventory_numbers)
    to_be_deleted = len(remove)
    print('Removing {} items'.format(to_be_deleted))
    if not dry_run:
        remove.delete()
