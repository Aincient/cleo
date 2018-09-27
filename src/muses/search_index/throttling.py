import datetime
import time
import logging

from django.core.cache import cache, caches
from django.core.exceptions import ImproperlyConfigured

from rest_framework.settings import api_settings
from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle

__all__ = (
    'SearchUserRateThrottle',
    'parse_rate',
    'get_scope_and_ident',
    'get_rate',
    'get_history',
    'get_cache_key',
)

LOGGER = logging.getLogger(__name__)

UNLIMITED_ACCESS_USER = 'unlimited_access_user'
AUTHENTICATED_USER = 'authenticated_user'
SUBSCRIBED_USER = 'subscribed_user'
SUBSCRIBED_GROUP_USER = 'subscribed_group_user'
SUPER_USER = 'super_user'
CACHE_FORMAT = 'throttle_%(scope)s_%(ident)s'

cache = caches['throttling']


def parse_rate(rate):
    """Given the request rate string, return a two tuple of:
    <allowed number of requests>, <period of time in seconds>
    """
    if rate is None:
        return (None, None)

    num, period = rate.split('/')
    num_requests = int(num)
    duration = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'j': 86400 * 30,
    }[period[0]]
    return num_requests, duration


def get_scope_and_ident(request):
    """Get scope and ident.

    :param request:
    :return:
    """
    # If user is not authenticated, do not continue
    if not request.user.is_authenticated:
        return None, None

    # If superuser
    if request.user.is_superuser:
        return SUPER_USER, request.user.pk
    else:
        # User with unlimited access
        try:
            if request.user.account_settings.unlimited_access:
                return UNLIMITED_ACCESS_USER, request.user.pk
        except Exception:
            pass

        # User with active subscription
        try:
            if request.user.account_settings.num_requests > 0:
                return SUBSCRIBED_USER, request.user.pk
        except Exception:
            pass

        # User belonging to a group with active subscription
        try:
            num_subscribed_groups = request \
                .user \
                .user_groups \
                .filter(
                    valid_from__lte=datetime.datetime.now(),
                    valid_until__gte=datetime.datetime.now()
                ) \
                .values_list('valid_from', 'valid_until')\
                .count()
            if num_subscribed_groups:
                return SUBSCRIBED_GROUP_USER, request.user.pk
        except Exception:
            pass

        # Finally, just an authenticated user
        return AUTHENTICATED_USER, request.user.pk


def get_rate(scope):
    """Get rate.

    :param scope:
    :return:
    """
    return api_settings.DEFAULT_THROTTLE_RATES[scope]


def get_cache_key(request, cache_format=CACHE_FORMAT, scope=None, ident=None):
    """Get cache key.

    :param request:
    :param cache_format:
    :param scope:
    :param ident:
    :return:
    """
    # If user is not authenticated, do not continue
    if not request.user.is_authenticated:
        return None

    if scope is None or ident is None:
        scope, ident = get_scope_and_ident(request)

    return cache_format % {
        'scope': scope,
        'ident': ident
    }


def get_history(request, cache_format=CACHE_FORMAT, scope=None, ident=None):
    """Get history.

    :param request:
    :param cache_format:
    :param scope:
    :param ident:
    :return:
    """
    if scope is None or ident is None:
        scope, ident = get_scope_and_ident(request)

    key = get_cache_key(request, cache_format, scope, ident)
    history = cache.get(key, [])
    now = time.time()
    rate = get_rate(scope)
    num_requests, duration = parse_rate(rate)
    while history and history[-1] <= now - duration:
        history.pop()
    return history


class SearchUserRateThrottle(SimpleRateThrottle):
    """Generic class.

    Having one big throttle class seems to work better.
    """

    scope = None
    rate = '3/j'
    scope_attr = 'throttle_scope'

    def __init__(self):
        # Override the usual SimpleRateThrottle, because we can't determine
        # the rate until called by the view.
        pass

    def parse_rate(self, rate):
        return parse_rate(rate)

    def get_rate(self, request, scope):
        """
        Determine the string representation of the allowed request rate.
        """
        # if not getattr(self, 'scope', None):
        #     msg = (
        #         "You must set either `.scope` or `.rate` for '%s' "
        #         "throttle" % self.__class__.__name__
        #     )
        #     raise ImproperlyConfigured(msg)

        try:
            return self.THROTTLE_RATES[scope]
        except KeyError:
            msg = "No default throttle rate set for '%s' scope" % scope
            raise ImproperlyConfigured(msg)

    def allow_request(self, request, view):
        # We can only determine the scope once we're called by the view.
        scope, ident = get_scope_and_ident(request)

        # If a view does not have a `throttle_scope` always allow the request
        if not scope:
            return True

        # Determine the allowed request rate as we normally would during
        # the `__init__` call.
        rate = self.get_rate(request, scope)
        num_requests, duration = self.parse_rate(rate)

        # We can now proceed as normal.
        if rate is None:
            return True

        key = self.get_cache_key(request, view)
        if key is None:
            return True

        history = self.cache.get(key, [])
        now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while history and history[-1] <= now - duration:
            history.pop()

        if len(history) >= num_requests:
            return self.throttle_failure()

        # If request user has credits left, we deduct 1 and save
        if request.user.account_settings.num_requests > 0:
            request.user.account_settings.num_requests -= 1
            request.user.account_settings.save()

        return self.throttle_success(key, now, history, duration)

    def get_cache_key(self, request, view):
        """Get cache key.

        :param request:
        :param view:
        :return:
        """
        return get_cache_key(
            request,
            self.cache_format
        )

    def throttle_success(self, key, now, history, duration):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        history.insert(0, now)
        self.cache.set(key, history, duration)
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False

    def wait(self):
        return None
