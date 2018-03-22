from django.core.exceptions import ImproperlyConfigured
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse

__all__ = ['config']


def required(name):
    from django.conf import settings
    result = getattr(settings, name, None)
    if result is None:
        raise ImproperlyConfigured('settings.{} required'.format(name))
    return result


def optional(name, default):
    from django.conf import settings
    return getattr(settings, name, default)


class Config(object):
    @property
    def FUTUPAYMENTS_RECIEPTS(self):
        return optional('FUTUPAYMENTS_RECIEPTS', False)

    @property
    def FUTUPAYMENTS_TEST_MODE(self):
        return optional('FUTUPAYMENTS_TEST_MODE', False)

    @property
    def FUTUPAYMENTS_HOST(self):
        return optional('FUTUPAYMENTS_HOST', 'https://secure.futubank.com')

    @property
    def FUTUPAYMENTS_MERCHANT_ID(self):
        return required('FUTUPAYMENTS_MERCHANT_ID')

    @property
    def FUTUPAYMENTS_SECRET_KEY(self):
        return required('FUTUPAYMENTS_SECRET_KEY')

    @property
    def FUTUPAYMENTS_SUCCESS_URL(self):
        from . import views
        return optional('FUTUPAYMENTS_SUCCESS_URL', reverse(views.success))

    @property
    def FUTUPAYMENTS_FAIL_URL(self):
        from . import views
        return optional('FUTUPAYMENTS_FAIL_URL', reverse(views.fail))


config = Config()
