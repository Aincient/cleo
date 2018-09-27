# Django settings for example project.
import os
import sys

from nine import versions

from .core import PROJECT_DIR, gettext


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
DEBUG_TOOLBAR = False
DEV = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': PROJECT_DIR(os.path.join('..', '..', 'db', 'example.db')),
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext("English")),  # Main language!
    # ('hy', gettext("Armenian")),
    ('nl', gettext("Dutch")),
    # ('ru', gettext("Russian")),
    # ('de', gettext("German")),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_DIR(os.path.join('..', '..', 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

LOCALE_PATHS = [
    PROJECT_DIR(os.path.join('..', 'locale')),
]

# Absolute filesystem path to the directory that contains all image
# classification models
IMAGE_CLASSIFICATION_DIR = os.path.abspath(os.path.join(BASE_DIR,
                                                        '..',
                                                        '..',
                                                        'src',
                                                        'muses',
                                                        'image_classifcation',
                                                        )
                                           )


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_DIR(os.path.join('..', '..', 'static'))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Wagtail site name
WAGTAIL_SITE_NAME = 'CLEO'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # PROJECT_DIR(os.path.join('..', '..', 'media', 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '12345a*a12Aa1a-a^1aaABabcdAB1+a1_abc*)a@(*_Aa1a123'

try:
    from .local_settings import DEBUG_TEMPLATE
except Exception as err:
    DEBUG_TEMPLATE = False

try:
    from .local_settings import USE_CACHED_TEMPLATE_LOADERS
except Exception as err:
    USE_CACHED_TEMPLATE_LOADERS = False

if USE_CACHED_TEMPLATE_LOADERS:

    _TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            # 'django.template.loaders.eggs.Loader',
        )),
    ]
else:

    _TEMPLATE_LOADERS = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        # 'django.template.loaders.eggs.Loader',
    ]

if versions.DJANGO_GTE_1_10:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'APP_DIRS': True,
            'DIRS': [PROJECT_DIR(os.path.join('..', 'templates'))],
            'OPTIONS': {
                'context_processors': [
                    "django.template.context_processors.debug",
                    'django.template.context_processors.request',
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "wagtailmenus.context_processors.wagtailmenus",
                    # "context_processors.testing",  # Testing
                ],
                'loaders': _TEMPLATE_LOADERS,
                'debug': DEBUG_TEMPLATE,
            }
        },
    ]
elif versions.DJANGO_GTE_1_8:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'APP_DIRS': True,
            'DIRS': [PROJECT_DIR(os.path.join('..', 'templates'))],
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.request",
                    "wagtailmenus.context_processors.wagtailmenus",
                    # "context_processors.testing",  # Testing
                ],
                'loaders': _TEMPLATE_LOADERS,
                'debug': DEBUG_TEMPLATE,
            }
        },
    ]
else:
    TEMPLATE_DEBUG = DEBUG_TEMPLATE

    # List of callables that know how to import templates from various
    # sources.
    TEMPLATE_LOADERS = _TEMPLATE_LOADERS

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
    )

    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or
        # "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        PROJECT_DIR(os.path.join('..', 'templates')),
    )

_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'wagtailtrans.middleware.TranslationMiddleware',
)

WAGTAILTRANS_SYNC_TREE = True
WAGTAILTRANS_LANGUAGES_PER_SITE = False

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

# FIXTURE_DIRS = (
#   PROJECT_DIR(os.path.join('..', 'fixtures'))
# )

INSTALLED_APPS = [
    # Django core and contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.redirects',

    # Third party apps
    'corsheaders',
    'rest_framework',  # REST framework
    'django_elasticsearch_dsl',  # Elasticsearch integration
    'django_elasticsearch_dsl_drf',  # Elasticsearch DRF integration
    'rest_framework.authtoken',
    'rest_auth',  # REST authentication/registration
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',

    'cities',  # Countries/cities app
    'imagekit',  # Image kit
    'mptt',  # Modified Preorder Tree Traversal for Django
    'memoize',  # Caching/memoization for functions and methods
    # 'invitations',  # Invitations
    'multi_email_field',  # Multi-emails field (for invitations)

    # Project apps
    'muses',  # Core
    'muses.collection',  # Collection
    'muses.cached_api_calls',  # Translation
    # 'muses.exporters.all',  # Exporter app
    # 'muses.exporters.coin',  # Exporter app
    'muses.exporters.naive',    # Exporter app
    'muses.exporters.material',    # Exporter app
    # 'muses.exporters.cluster',
    'muses.importers.rmo_nl',  # Importer app
    'muses.importers.brooklynmuseum_org',  # Importer app
    'muses.importers.thewalters_org',  # Importer app
    'muses.importers.metmuseum_org',  # Importer app
    'muses.search_index',  # Search app
    'muses.user_account',  # User account additions
    'muses.payments_subscriptions',  # Payments and subscriptions app
    'muses.invitations_addons',  # Invitations add-ons
    'muses.imagekit_addons',  # django-imagekit add-ons

    # Other project specific apps
    'assets',  # Static files
    'webpack_loader',

    'cms',
    
    # Wagtail 
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'wagtail.contrib.modeladmin',
    'wagtailtrans',
    'wagtailmenus',

    'modelcluster',
    'taggit',
]

# ***********************************************************************
# *************************** Cache settings ****************************
# ***********************************************************************

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    'throttling': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# ***********************************************************************
# ************************ django-rest-framework ************************
# ***********************************************************************

THROTTLE_NAME_SUPER_USER = 'super_user'
THROTTLE_NAME_UNLIMITED_ACCESS_USER = 'unlimited_access_user'
THROTTLE_NAME_SUBSCRIBED_USER = 'subscribed_user'
THROTTLE_NAME_SUBSCRIBED_GROUP_USER = 'subscribed_group_user'
THROTTLE_NAME_AUTHENTICATED_USER = 'authenticated_user'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'ORDERING_PARAM': 'ordering',
    'DEFAULT_THROTTLE_RATES': {
        THROTTLE_NAME_SUPER_USER: '999999999/j',
        THROTTLE_NAME_UNLIMITED_ACCESS_USER: '500000/j',
        THROTTLE_NAME_SUBSCRIBED_USER: '500000/j',
        THROTTLE_NAME_SUBSCRIBED_GROUP_USER: '500000/j',
        THROTTLE_NAME_AUTHENTICATED_USER: '50/j',
    },
}

# ***********************************************************************
# ******************* django-rest-auth and django-allauth ***************
# ***********************************************************************

# Pure django auth and registration related settings
LOGIN_URL = '/search/login/'
LOGIN_ERROR_URL = '/search/login/'
LOGOUT_URL = '/search/logout/'
LOGIN_REDIRECT_URL = '/search/login/'

# django-rest-auth config
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER':
        'muses.user_account.rest_auth_serializers.CustomUserDetailsSerializer',

}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER':
        'muses.user_account.rest_auth_serializers.CustomRegisterSerializer',
}

# django-allauth config
ACCOUNT_LOGOUT_ON_GET = True

# ***********************************************************************
# *************************** django-invitations ************************
# ***********************************************************************

# ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'
INVITATIONS_INVITATION_MODEL = 'invitations_addons.Invitation'
INVITATIONS_SIGNUP_REDIRECT = '/search/register'
# ***********************************************************************
# *************************** Elasticsearch *****************************
# ***********************************************************************

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200',
        'timeout': 30,
        # 'http_auth': 'elastic:changeme',
    },
}

# Name of the Elasticsearch index
ELASTICSEARCH_INDEX_NAMES = {
    'muses.search_index.documents.collection_item': 'collection_item',
}

# ***********************************************************************
# ***************************** Synonyms ********************************
# ***********************************************************************
SYNONYMS = {
    'en': PROJECT_DIR(os.path.join('..', '..', 'synonyms', 'raw', 'en.txt')),
    'nl': PROJECT_DIR(os.path.join('..', '..', 'synonyms', 'raw', 'nl.txt')),
}

# ***********************************************************************
# ***************************** Mollie **********************************
# ***********************************************************************

MOLLIE_API_KEY = 'not-provided'
SITE_DOMAIN = 'http://foobar.com'  # fill in for correct env

# ***********************************************************************
# ************************* django-imagekit *****************************
# ***********************************************************************

# ImageKit configuration
IMAGEKIT_CACHEFILE_DIR = os.path.join(
    MEDIA_ROOT,
    'collection_images_medium'
)
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'muses.collection.namers.same_name_custom_dir'

# ***********************************************************************
# ************************* django-cors-headers *************************
# ***********************************************************************

# CORS headers config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'localhost:8000',
    '127.0.0.1:3000',
    '127.0.0.1:8000',
    'http://aincient-acc.gw20e.com',
)

# ***********************************************************************
# ******************************* Google ********************************
# ***********************************************************************

# Google API configuration
GOOGLE_API_KEY = 'Not provided'

# ***********************************************************************
# *************************** django-cities *****************************
# ***********************************************************************

# Django-cities configuration
CITIES_DATA_DIR = os.path.join(
    MEDIA_ROOT,
    'cities/data/'
)

FIREFOX_BIN_PATH = None

# ***********************************************************************
# ************************ muses/cleo (this app) ************************
# ***********************************************************************

# Muses config
MUSES_CONFIG = {
    'importers': {
        'rmo_nl': {
            'url': 'http://api.rmo.nl:17521/action=get&command=search&query=*egypt*&range=1-1000000&fields=*',  # NOQA
            'tmp_dir': PROJECT_DIR(
                os.path.join('..', '..', 'import', 'rmo_nl')
            ),
        },
        'brooklynmuseum_org': {
            'base_url': 'https://www.brooklynmuseum.org/',
            'object_list_url': '/api/v2/object/?collection_id=5&limit=35',
            'geographical_location_list_url': '/api/v2/geographical-location/'
                                              '?limit=35',
            'object_images_url': '/api/v2/object/{}/image/',
            'api_key': 'not-provided',
            'tmp_dir': PROJECT_DIR(
                os.path.join('..', '..', 'import', 'brooklynmuseum_org')
            ),
        },
        'thewalters_org': {
            'base_url': 'http://api.thewalters.org/',
            'object_list_url': '/v1/objects.json?creator=Egyptian',
            'object_detail_url': '/v1/objects/{}.json',
            'object_images_url': '/v1/objects/{}/images.json',
            'api_key': 'not-provided',
            'tmp_dir': PROJECT_DIR(
                os.path.join('..', '..', 'import', 'thewalters_org')
            ),
        },
        'metmuseum_org': {
            'object_list_url': 'https://github.com/metmuseum/openaccess/raw/master/MetObjects.csv',  # NOQA
            'object_images_url': 'http://www.metmuseum.org/api/Collection/additionalImages?crdId={}&page=1&perPage=10',  # NOQA
            'tmp_dir': PROJECT_DIR(
                os.path.join('..', '..', 'import', 'metmuseum_org')
            ),
        },
    },
    'classification': {
        'naive_classification': {
            'model_path': os.path.join(
                BASE_DIR,
                '..',
                '..',
                'src',
                'muses',
                'naive_classification',
                'models',
                'new_model_f1_finetuned_2_trained.h5'
            )
        },
    },
}

# ***********************************************************************
# ************************ Logging configuration ************************
# ***********************************************************************

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['all_log'],
    },
    'formatters': {
        'verbose': {
            'format': '\n%(levelname)s %(asctime)s [%(pathname)s:%(lineno)s] '
                      '%(message)s'
        },
        'simple': {
            'format': '\n%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'all_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/all.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/django.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'django_request_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/django_request.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
        'muses_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_DIR("../../logs/muses.log"),
            'maxBytes': 1048576,
            'backupCount': 99,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['django_request_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['django_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'muses': {
            'handlers': ['console', 'muses_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ***********************************************************************
# ****************** django-debug-toolbar configuration *****************
# ***********************************************************************

# Do not put any settings below this line
try:
    from .local_settings import DEBUG, DEBUG_TOOLBAR
except ImportError:
    pass

if DEBUG and DEBUG_TOOLBAR:
    try:
        # Make sure the django-debug-toolbar is installed
        import debug_toolbar

        # debug_toolbar
        _MIDDLEWARE_CLASSES += (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
        )

        INSTALLED_APPS += (
            'debug_toolbar',
            'elastic_panel',
        )

        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
            'JQUERY_URL': STATIC_URL + 'rest_framework/js/jquery-1.12.4.min.js',
        }

        DEBUG_TOOLBAR_PANELS = (
            # Defaults
            'debug_toolbar.panels.timer.TimerPanel',
            'debug_toolbar.panels.settings.SettingsPanel',
            'debug_toolbar.panels.headers.HeadersPanel',
            'debug_toolbar.panels.request.RequestPanel',
            'debug_toolbar.panels.sql.SQLPanel',
            'debug_toolbar.panels.staticfiles.StaticFilesPanel',
            'debug_toolbar.panels.templates.TemplatesPanel',
            'debug_toolbar.panels.cache.CachePanel',
            'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.logging.LoggingPanel',
            'debug_toolbar.panels.redirects.RedirectsPanel',
            # Additional
            'elastic_panel.panel.ElasticDebugPanel',
        )

    except ImportError:
        pass

# ***********************************************************************
# ************************* Other configurations ************************
# ***********************************************************************

if versions.DJANGO_GTE_2_0:
    MIDDLEWARE = _MIDDLEWARE_CLASSES
else:
    MIDDLEWARE_CLASSES = _MIDDLEWARE_CLASSES

# Make the `muses` package available without
# installation or development.
if DEV:
    app_source_path = os.environ.get(
        'APP_SOURCE_PATH',
        'src'
    )
    # sys.path.insert(0, os.path.abspath('src'))
    sys.path.insert(0, os.path.abspath(app_source_path))

# WEBPACK_LOADER = {
#     'DEFAULT': {
#             'BUNDLE_DIR_NAME': '',
#             'STATS_FILE': os.path.join('../../../..', 'webpack-stats.json'),
#     }
# }
