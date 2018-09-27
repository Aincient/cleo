import time
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.middleware import csrf
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template import loader


import logging
import Mollie

import requests

from six.moves.urllib.parse import urljoin

from muses.payments_subscriptions.models import Order

logger = logging.getLogger(__name__)


def base(request):
    """Base  (/) view."""

    return render(
        request,
        'index.html'
    )


def checkout(request):
    """Checkout.

    :param request:
    :return:
    """


class CSRFToken(View):
    """
    View to get a CSRF token and set it as a csrftoken cookie.
    token is returned as well.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFToken, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        token = csrf.get_token(request)
        response = JsonResponse({'token': token})
        response.set_cookie('csrftoken', token)
        return response


@csrf_exempt
def mollie_webhook(request):
    """
    update order payment status

    :param request:
    :return:
    """
    try:
        mollie = Mollie.API.Client()
        mollie.setApiKey(settings.MOLLIE_API_KEY)

        payment_id = request.POST.get('id', None)
        if payment_id == None:
            return HttpResponseServerError('no payment id in webhook call')
        payment = mollie.payments.get(payment_id)
        order_nr = payment['metadata']['order_nr']
        order = Order.objects.get(pk=order_nr)
        order.status = payment['status']
        order.save()

        if payment.isPaid():
            # At this point you'd probably want to start the process of
            # delivering the product to the customer.

            logger.info('Paid')
            order.user.account_settings.num_requests += order.product.num_requests
            order.user.account_settings.save()

            html_message = loader.render_to_string(
                'payment/invoice_mail.html',
                {
                    'ordernr': order_nr
                }
            )
            send_mail(
                'Bevestiging van uw bestelling bij Cleo (onderdeel van Aincient)',
                'message',
                'cleo@aincient.org',
                [order.user.email,],
                fail_silently=True,
                html_message=html_message
            )
        elif payment.isPending():
            #
            # The payment has started but is not complete yet.
            #
            logger.info('Pending')
        elif payment.isOpen():
            #
            # The payment has not started yet. Wait for it.
            #
            logger.info('Open')
        else:
            # The payment isn't paid, pending nor open. We can assume it was
            # aborted.
            logger.info('Cancelled')
        return HttpResponse("<h1>i say 200</h1>")
    except Mollie.API.Error as e:
        logger.error('API call failed: ' + str(e))
        return HttpResponseServerError(e)


def order_redirect(request, order_id):
    logger.info("order complete: {0}".format(order_id))
    return redirect('/search/')


# def home(request, target_language='en'):
#     """Home.
#
#     :param request:
#     :param target_language:
#     :return:
#     """
#     base_url = request.get_raw_uri()
#     url = urljoin(base_url, '/pages/')
#     url = urljoin(url, '{}'.format(target_language))
#     response = requests.get(url)
#     response_text = response \
#         .text \
#         .replace(
#             '"/{}/'.format(target_language),
#             '"/pages/{}/'.format(target_language)
#         ) \
#         .replace(
#             "'/{}/".format(target_language),
#             "'/pages/{}/".format(target_language)
#         )
#     return HttpResponse(response_text)
