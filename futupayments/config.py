from __future__ import absolute_import
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from . import views


FUTUPAYMENTS_TEST_MODE = getattr(settings, 'FUTUPAYMENTS_TEST_MODE', True)

if FUTUPAYMENTS_TEST_MODE:
    default_url = 'https://secure.futubank.com/testing-pay/'
else:
    default_url = 'https://secure.futubank.com/pay/'

FUTUPAYMENTS_URL = getattr(settings, 'FUTUPAYMENTS_URL', default_url)

FUTUPAYMENTS_MERCHANT_ID = getattr(settings, 'FUTUPAYMENTS_MERCHANT_ID', None)
if not FUTUPAYMENTS_MERCHANT_ID:
    raise ImproperlyConfigured('settings.FUTUPAYMENTS_MERCHANT_ID required')

FUTUPAYMENTS_SECRET_KEY = getattr(settings, 'FUTUPAYMENTS_SECRET_KEY', None)
if not FUTUPAYMENTS_SECRET_KEY:
    raise ImproperlyConfigured('settings.FUTUPAYMENTS_SECRET_KEY required')

FUTUPAYMENTS_SUCCESS_URL = getattr(settings, 'FUTUPAYMENTS_SUCCESS_URL', None)
if not FUTUPAYMENTS_SUCCESS_URL:
    FUTUPAYMENTS_SUCCESS_URL = reverse(views.success)

FUTUPAYMENTS_FAIL_URL = getattr(settings, 'FUTUPAYMENTS_FAIL_URL', None)
if not FUTUPAYMENTS_FAIL_URL:
    FUTUPAYMENTS_FAIL_URL = reverse(views.fail)

