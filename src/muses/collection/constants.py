__all__ = (
    'DEFAULT_COPY_FIELDS',
    'DEFAULT_TRANSLATED_FIELDS',
    'ALLOWED_COPY_FIELDS',
    'ALLOWED_TRANSLATED_FIELDS',
    'NON_TRANSLATABLE_FIELDS',
)

# Some fields shall remain as is (without translation or copying).
# Please, never attempt to translate the following fields:
# - references

# Default translated fields.
DEFAULT_TRANSLATED_FIELDS = (
    'acquired',
    'city',
    'classification',
    'country',
    'department',
    'description',
    'dimensions',
    'dynasty',
    'keywords',
    'material',
    'object_type',
    'period',
    'reign',
    'title',

    # New fields
    'credit_line',
    'region',
    'sub_region',
    'locale',
    'excavation',
    'museum_collection',
    'style',
    'culture',
    'inscriptions',
    'provenance',
    'exhibitions',
)

ALLOWED_TRANSLATED_FIELDS = DEFAULT_TRANSLATED_FIELDS + (
    'site_found',
)

# Since
DEFAULT_COPY_FIELDS = (
    'acquired',
    'city',
    'classification',
    'country',
    'description',
    'dynasty',
    'keywords',
    'material',
    'object_type',
    'period',
    'reign',
    'title',

    # New fields
    'credit_line',
    'region',
    'sub_region',
    'locale',
    'excavation',
    'museum_collection',
    'style',
    'culture',
    'inscriptions',
    'provenance',
    'exhibitions',
)

ALLOWED_COPY_FIELDS = DEFAULT_COPY_FIELDS + (
    'site_found',
)

NON_TRANSLATABLE_FIELDS = (
    'geo_location',
    'accession_date',
)
