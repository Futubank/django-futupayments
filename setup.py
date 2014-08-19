from distutils.core import setup
import re


def get_version():
    init_py = open('futupayments/__init__.py').read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
    return metadata['version']

setup(
    name='django-futupayments',
    version=get_version(),
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
