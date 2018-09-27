from django.conf import settings
from elasticsearch_dsl import analyzer, token_filter

from .helpers import read_synonyms

__all__ = (
    'html_strip',
    'synonym_tokenfilter_en',
    'synonym_tokenfilter_nl',
    'html_strip_synonyms_en',
    'html_strip_synonyms_nl',
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=[
        "standard",
        "lowercase",
        "stop",
        "snowball",
    ],
    char_filter=["html_strip"]
)


synonym_tokenfilter_en = token_filter(
    'synonym_tokenfilter',
    'synonym',
    # synonyms=[
    #     'scarab, artur',  # <-- important
    # ],
    synonyms=read_synonyms(settings.SYNONYMS['en'])
)


synonym_tokenfilter_nl = token_filter(
    'synonym_tokenfilter',
    'synonym',
    # synonyms=[
    #     'scarab, artur',  # <-- important
    # ],
    synonyms=read_synonyms(settings.SYNONYMS['nl'])
)


html_strip_synonyms_en = analyzer(
    'text_analyzer',
    tokenizer='standard',
    filter=[
        # The ORDER is important here.
        'standard',
        'lowercase',
        'stop',
        synonym_tokenfilter_en,
        # Note! 'snowball' comes after 'synonym_tokenfilter'
        'snowball',
    ],
    char_filter=[
        'html_strip',
    ]
)


html_strip_synonyms_nl = analyzer(
    'text_analyzer',
    tokenizer='standard',
    filter=[
        # The ORDER is important here.
        'standard',
        'lowercase',
        'stop',
        synonym_tokenfilter_nl,
        # Note! 'snowball' comes after 'synonym_tokenfilter'
        'snowball',
    ],
    char_filter=[
        'html_strip',
    ]
)
