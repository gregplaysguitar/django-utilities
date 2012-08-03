import utilities
from setuptools import setup, find_packages
from setuptools.command.test import test

setup(
    name='django-utilities',
    version=utilities.__version__,
    description='My own collection of django utilities',
    long_description=open('readme.markdown').read(),
    author='Greg Brown',
    author_email='greg@gregbrown.co.nz',
    url='https://github.com/gregplaysguitar/django-utilities',
    packages=find_packages(exclude=['tests', 'tests.*']),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
)
