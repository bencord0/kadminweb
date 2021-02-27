from pathlib import Path
from setuptools import find_packages, setup


def find_templates(directory):
    return [
        str(template.relative_to(directory))
        for template
        in Path(directory).glob('**/*.html')
    ]


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
    version='0.1.0',
    author='Ben Cordero',
    author_email='bencord0@condi.me',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        "django_kerberos": find_templates('src/django_kerberos'),
        "kadminweb": find_templates('src/kadminweb'),
    },
    install_requires=install_requires,
    extras_require=extras_require,
)
