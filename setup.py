#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from distutils.command.install_data import install_data
#from pip._internal.req import parse_requirements

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

cmdclass = {'install_data': install_data}
data_files = [('/etc/MissingTVShows/', ['etc/tvshows.conf', 'etc/logging.conf']), ('/usr/local/etc/bash_completion.d/', ['etc/missingTVShows-completion.bash'])]
# install_reqs = parse_requirements('requirements.txt', session="test")
# reqs = [str(ir.requirement) for ir in install_reqs]
reqs = read('requirements.txt').splitlines()
tests_require = ['nose']


setup(
    name="mtvs",
    version="1.2.2.dev0",
    author="Andreas Ruppen",
    author_email="andreas.ruppen@gmail.com",
    description="Manages Kodi TVShows",
    license="Apache",
    keywords="kodi, tvshows, xbmc",
    url="https://github.com/digsim/missingTvShows",
    packages=find_packages('src', exclude=['contrib', 'docs', '*.tests*']),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'missingtvshows=mtvs.main:main',
        ],
    },
    cmdclass=cmdclass,
    include_package_data=True,
    install_requires=reqs,
    test_suite='nose.collector',
    tests_require=tests_require,
    long_description=read('README.rst'),
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        'Intended Audience :: Developers',
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    platforms='any',
)
