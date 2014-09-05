# -*- coding: utf-8 -*-

import sys
import os

from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

settings.configure(
    INSTALLED_APPS=('futupayments',),
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:',
        }
    },
    FUTUPAYMENTS_MERCHANT_ID='1',
    FUTUPAYMENTS_SECRET_KEY = '1',
    FUTUPAYMENTS_TEST_MODE = True,
    ROOT_URLCONF='example.example.urls',
    MIDDLEWARE_CLASSES=(),
)

if __name__ == "__main__":
    try:
        from django.apps import apps
    except ImportError:
        pass
    else:
        apps.populate(settings.INSTALLED_APPS)
    call_command('test', 'futupayments')
