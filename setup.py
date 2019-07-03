#!/usr/bin/env python
from distutils.core import setup

long_description = """
Simple tool to manage media files for fixtures.

See the repo home for usage instructions at
https://github.com/leetrout/django-fixturemedia/
"""

setup(
    name='django-fixture-media',
    version='0.2',
    description='Simple tool to manage media files for fixtures.',
    long_description=long_description,
    author='Lee Trout',
    author_email='leetrout@gmail.com',
    url='https://github.com/leetrout/django-fixturemedia/',
    packages=[
        'fixture_media',
        'fixture_media.management',
        'fixture_media.management.commands'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
)
