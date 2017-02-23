#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
from distutils.command.install_data import install_data
from pip.req import parse_requirements


cmdclass = {'install_data': install_data}
data_files = [('/etc/MissingTVShows/', ['etc/tvshows.cfg', 'etc/logging.conf']), ('/usr/local/etc/bash_completion.d/', ['etc/missingTVShows-completion.bash'])]
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
tests_require = ['nose']

if sys.version_info[:2] == (2, 6):
    # Python unittest2 only needed for Python 2.6
    tests_require.append('unittest2')
    # OrderedDict was added in 2.7
    reqs.append('ordereddict')





# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mtvs",
    version="1.2.1.dev0",
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    platforms='any',
)
