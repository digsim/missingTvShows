---
title: Missing TV Shows for Kodi
---

The [missingTvShows](https://github.com/digsim/missingTvShows) compares
the locally available tv show episodes managed by Kodi with the official
ones avaialbe on the tvdb and prints a summary containing 4 sections: \*
TV Show Seasons which where all published episodes are locally available
and \* none has been watched \* some have already been watched \* TV
Show Seasons which where some published episodes are not available
locally and \* none has been watched \* some have already been watched

------------------------------------------------------------------------

Build status:

[![missingtvshows test status](https://github.com/digsim/missingTvShows/actions/workflows/master-workflow.yaml/badge.svg)](https://github.com/digsim/missingTvShows/actions)

Coverage:

[![image](https://coveralls.io/repos/digsim/missingTvShows/badge.svg?branch=master)](https://coveralls.io/r/digsim/missingTvShows?branch=master)

Homepage
: <http://missingtvshows.readthedocs.io/en/latest/>

Code
: <https://github.com/digsim/missingTvShows>

Dependencies
: [tvdb-v4-official]()
: [colorama](https://pypi.org/pypi/colorama)
: [SQLAlchemy](https://pypi.org/pypi/SQLAlchemy)
: [SQLAlchemy-Utils](http://pypi.org/pypi/sqlalchemy-utils)
: [mysqlclient](http://pypi.org/pypi/sqlalchemy-utils)
: [progressbar2](http://pypi.org/pypi/sqlalchemy-utils) and
: [pyparsing]()

Compatible with
: Python 3.9+

License
: [APACHE](http://www.apache.org/licenses/LICENSE-2.0.txt)

------------------------------------------------------------------------

# Installation

* Create virtualenv `virtualenv -p /opt/homebrew/bin/python3.12 venv-312`
* Active virtualenv `source venv-312/bin/activate.bash`
* Install software locally `pip install .`

# Usage

Simply launch [missingTvShows]{.title-ref} to get help and instructions
on how to use the tool

```bash
└─\> master 🕙 12:29:38 ❯ missingTvShows -h usage: missingtvshows
\[-h\] \[-v\] {sync} \...

Checks missing TV Show Episodes based on the list of available
Episodes on thetvdb.com

positional arguments: {sync} commands sync sync Kodi and TVDB

options: -h, \--help show this help message and exit -v, \--version
show program\'s version number and exit

missingtvshows {command} -h for help on individual commands
```

The `missingTvShows` relies on two config files sitting in
`~/.MissingTVShows`:

-   `tvshows.conf` : main configuration file of missingTvShows.
-   `logging.conf`: logging configuration

These two files are created on the first run and at least the
`tvshows.conf` need to be adapted accordingly:


```
[Config]
api_key: <thetvdb_api_key>
tvdbdb:  ./tvdbdb.db # location of the sqlite3 cache of tvdb information relative to this file
[Database] # coordinates of the Kodi DB, supports mysql and sqlite3
#dialect: sqlite
#db: /Volumes/Data/ruppena/Documents/Programming/Python/missing_tv_shows_for_xbmc/test.db
dialect: mysql # one of mysql, sqlite
db: MyVideos121 # in case of mysql the name of the DB in case of sqlite3 the full filepath
user: <mysql_user>
passwd: <mysql_passwor>
hostname: <mysql_host>
port:<mysql_port>
```

and it produces the following two files (also in `~/.MissingTVShows`):

* `tvdbdb.db` : cached thetvdb information
* `tvshows.log` : log of the last run


[![image](https://travis-ci.org/digsim/missingTvShows.svg?branch=master)](https://travis-ci.org/digsim/missingTvShows)

## Roadmap

-   2.0: Progress bar

## Test Coverage Report

Output from coverage test:

```
Name                               Stmts   Miss  Cover
------------------------------------------------------
src/mtvs/Kodi/__init__.py              6      2    67%
src/mtvs/Kodi/missing_tvshows.py     224    180    20%
src/mtvs/__init__.py                   2      0   100%
src/mtvs/main/__init__.py              5      5     0%
src/mtvs/main/main.py                 81     81     0%
src/mtvs/main/mainImpl.py             78     78     0%
src/mtvs/utils/__init__.py             0      0   100%
src/mtvs/utils/utilities.py           52     52     0%
------------------------------------------------------
TOTAL                                448    398    11%
```
