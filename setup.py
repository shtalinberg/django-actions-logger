import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-actions-logger',
    version='0.1.0',
    packages=['actionslog'],
    include_package_data=True,
    package_dir={'': 'src'},
    url='https://github.com/shtalinberg/django-actions-logger',
    license='MIT',
    author='Oleksandr Shtalinberg',
    author_email='shtalinberg@ukr.net',
    description='A Django app that keeps a log of user actions or changes in objects',
    long_description=README,
    install_requires=[
        'Django>=1.8',
        'django-jsonfield>=0.9.15',
    ]
)
