from __future__ import absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

__all__ = ['config']

_FUTUPAYMENTS_TEST_MODE = getattr(settings, 'FUTUPAYMENTS_TEST_MODE', False)
if _FUTUPAYMENTS_TEST_MODE:
    default_url = 'https://secure.futubank.com/testing-pay/'
else:
    default_url = 'https://secure.futubank.com/pay/'


def required(name):
    result = getattr(settings, name, None)
    if result is None:
        raise ImproperlyConfigured('settings.%s required' % name)
    return result


class Config(object):
    FUTUPAYMENTS_TEST_MODE = _FUTUPAYMENTS_TEST_MODE

    FUTUPAYMENTS_URL = getattr(settings, 'FUTUPAYMENTS_URL', default_url)

    FUTUPAYMENTS_MERCHANT_ID = required('FUTUPAYMENTS_MERCHANT_ID')

    FUTUPAYMENTS_SECRET_KEY = required('FUTUPAYMENTS_SECRET_KEY')

    @property
    def FUTUPAYMENTS_SUCCESS_URL(self):
        from . import views
        return getattr(settings, 'FUTUPAYMENTS_SUCCESS_URL', reverse(views.success))

    @property
    def FUTUPAYMENTS_FAIL_URL(self):
        from . import views
        return getattr(settings, 'FUTUPAYMENTS_FAIL_URL', reverse(views.fail))

config = Config()

