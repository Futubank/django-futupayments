import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

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

FUTUPAYMENTS_MERCHANT_ID = '1'
FUTUPAYMENTS_SECRET_KEY = '1'
FUTUPAYMENTS_TEST_MODE = True

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'), )
