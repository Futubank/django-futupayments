from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

__all__ = ['config']


def required(name):
    result = getattr(settings, name, None)
    if result is None:
        raise ImproperlyConfigured('settings.{} required'.format(name))
    return result


class Config(object):
    FUTUPAYMENTS_TEST_MODE = getattr(settings, 'FUTUPAYMENTS_TEST_MODE', False)
    FUTUPAYMENTS_HOST = getattr(settings, 'FUTUPAYMENTS_HOST', 'https://secure.futubank.com')  # noqa
    FUTUPAYMENTS_MERCHANT_ID = required('FUTUPAYMENTS_MERCHANT_ID')
    FUTUPAYMENTS_SECRET_KEY = required('FUTUPAYMENTS_SECRET_KEY')

    @property
    def FUTUPAYMENTS_SUCCESS_URL(self):
        from . import views
        return getattr(settings, 'FUTUPAYMENTS_SUCCESS_URL', reverse(views.success))  # noqa

    @property
    def FUTUPAYMENTS_FAIL_URL(self):
        from . import views
        return getattr(settings, 'FUTUPAYMENTS_FAIL_URL', reverse(views.fail))


config = Config()
