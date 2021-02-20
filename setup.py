import os
from setuptools import find_packages, setup

install_requires = [
    'django',
    'dj-database-url',
    'pykerberos',
]

extras_require = {
    'tests': ['pytest'],
    'webserver': ['gunicorn', 'whitenoise'],
}

setup(
    name='kadminweb',
    version='0.0.1',
    author='Ben Cordero',
    author_email='bencord0@condi.me',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    extras_require=extras_require,
)
