==========================================================
Missing TV Shows for Kodi
==========================================================

The `missingtvshows`_ verifies the locally available episodes for all Kodi Series

----

    :Homepage: https://github.com/digsim/missingTvShows
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

    py35 runtests: commands[1] | coverage report
    Name                              Stmts   Miss  Cover
    -----------------------------------------------------
    src/adnitc/__init__.py                2      0   100%
    src/adnitc/itc/__init__.py            0      0   100%
    src/adnitc/itc/calendar2itc.py      138     14    90%
    src/adnitc/itc/calendarEvent.py      96      4    96%
    src/adnitc/itc/itcClient.py          66     14    79%
    src/adnitc/main/__init__.py           5      5     0%
    src/adnitc/main/main.py              81     81     0%
    src/adnitc/main/mainImpl.py         197    197     0%
    src/adnitc/utils/__init__.py          0      0   100%
    src/adnitc/utils/utilities.py        28     28     0%
    -----------------------------------------------------
    TOTAL                               613    343    44%
