import os
import re
from setuptools import setup, find_packages


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
        return readme.read()


def version():
    pattern = re.compile(r'__version__ = \'([\d\.]+)\'')
    with open(os.path.join('django_logging', '__init__.py')) as f:
        data = f.read()
        return re.search(pattern, data).group(1)


setup(
    name='django-logging',
    version=version(),
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    description='A simple Django app to log requests/responses in various formats, such as JSON.',
    long_description=readme(),
    url='https://github.com/cipriantarta/django-logging',
    author='Ciprian Tarta',
    author_email='me@cipriantarta.ro',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django logging json'
)
