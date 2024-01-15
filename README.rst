==========================================================
Missing TV Shows for Kodi
==========================================================

The `missingtvshows`_ verifies the locally available episodes for all Kodi Series

----

    :Homepage: http://missingtvshows.readthedocs.io/en/latest/
    :Code: https://github.com/digsim/missingTvShows
    :Mailing list: https://github.com/digsim/missingTvShows
    :Dependencies: `pytvdbapi`_ `colorama`_ `sqlalchemy`_ `sqlalchemy-utils`_ `six`_ `mysqlclient`_  `progressbar2`_ and `setuptools`_
    :Compatible with: Python 2.6, 2.7 and 3.3+
    :License: `APACHE`_

----


.. image:: https://travis-ci.org/digsim/missingTvShows.svg?branch=master
    :target: https://travis-ci.org/digsim/missingTvShows


Roadmap
=======

- 2.0: Progress bar, read ITC entry, limit amout of written entries, limit past entries


.. _`pytvdbapi`: http://pypi.python.org/pypi/pytvdbapi
.. _`missingtvshows`: https://github.com/digsim/missingTvShows
.. _`adnitc`: https://adnitc.gotdns.org/
.. _`colorama`: https://pypi.python.org/pypi/colorama
.. _`sqlalchemy`: https://pypi.python.org/pypi/SQLAlchemy
.. _`sqlalchemy-utils`: http://pypi.python.org/pypi/sqlalchemy-utils
.. _`mysqlclient`: http://pypi.python.org/pypi/sqlalchemy-utils
.. _`progressbar2`: http://pypi.python.org/pypi/sqlalchemy-utils
.. _`six`: http://pythonhosted.org/six/
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`APACHE`: http://www.apache.org/licenses/LICENSE-2.0.txt


Test Coverage Report
====================

Output from coverage test::

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
