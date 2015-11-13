import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-logging',
    version='1.0',
    packages=['django-logging'],
    include_package_data=True,
    license='GNU License',  # example license
    description='A simple Django app to log requests/responses in various formats, such as JSON.',
    long_description=README,
    url='https://github.com/cipriantarta/django-logging',
    author='Ciprian Tarta',
    author_email='me@cipriantarta.ro',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
