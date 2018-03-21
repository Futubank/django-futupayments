import re
from distutils.core import setup


def get_version():
    init_py = open('futupayments/__init__.py').read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
    return metadata['version']

setup(
    name='django-futupayments',
    version=get_version(),
    author='Maxim Oransky',
    license='MIT license',
    author_email='maxim.oransky@gmail.com',
    packages=[
        'futupayments',
        'futupayments.migrations',
    ],
    package_data={
        'futupayments': ['templates/futupayments/*'],
    },
    url='https://github.com/Futubank/django-futupayments',
    requires=['django (>= 1.7)'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
