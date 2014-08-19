from distutils.core import setup


setup(
    name='django-futupayments',
    version='0.1',
    author='Maxim Oransky',
    author_email='om@futubank.com',
    packages=[
        'futupayments',
        'futupayments.migrations',
    ],
    package_data={
        'futupayments': ['templates/futupayments/*'],
    },
    url='https://github.com/Futubank/django-futupayments',
    requires=['django (>= 1.3)'],
)
