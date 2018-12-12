import os
from setuptools import setup

PROJECT_NAME = 'actionslog'
ROOT = os.path.abspath(os.path.dirname(__file__))
VENV = os.path.join(ROOT, '.venv')
VENV_LINK = os.path.join(VENV, 'local')

install_requires = [
    'Django>=1.8',
    'django-jsonfield>=0.9.15',
    'pytz>=2015.7',
]

project = __import__(PROJECT_NAME)

root_dir = os.path.dirname(__file__)


if root_dir:
    os.chdir(root_dir)

data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))

with open(os.path.join(root_dir, 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-actions-logger',
    version=project.get_version(),
    packages=['actionslog', 'actionslog.migrations'],
    include_package_data=True,
    url='https://github.com/shtalinberg/django-actions-logger',
    license='MIT',
    author='Oleksandr Shtalinberg',
    author_email='shtalinberg@ukr.net',
    description='A Django app that keeps a log of user actions or changes in objects',
    long_description=README,
    keywords='django actions log action logger',
    install_requires=install_requires,
    package_data={PROJECT_NAME: data_files},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
