DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sqlite',
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'

SECRET_KEY = 'futugate-example'

ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'

INSTALLED_APPS = (
    'app',
    'futupayments',
)

FUTUPAYMENTS_MERCHANT_ID = '27'
FUTUPAYMENTS_SECRET_KEY = '1'
FUTUPAYMENTS_TEST_MODE = True

import os

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'), )
