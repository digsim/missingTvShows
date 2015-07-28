#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from distutils.command.install_data import install_data
from pip.req import parse_requirements


scripts = ['bin/missingTVShows']
cmdclass = {'install_data': install_data}
data_files = [('/etc/MissingTVShows/', ['etc/tvshows.cfg', 'etc/logging.conf']), ('/usr/local/etc/bash_completion.d/', ['etc/missingTVShows-completion.bash'])]
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]



# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="missingTvShows",
    version="1.1",
    author="Andreas Ruppen",
    author_email="andreas.ruppen@gmail.com",
    description="Manages Kodi TVShows",
    license="Apache",
    keywords="kodi, tvshows, xbmc",
    url="https://github.com/digsim/missing_tv_shows_for_xbmc",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    scripts=scripts,
    cmdclass=cmdclass,
    data_files=data_files,
    install_requires=reqs,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        'Intended Audience :: Developers',
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
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
