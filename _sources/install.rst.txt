Installation
====================

From Download
--------------

The simplest way to use *missingtvshows* is to download the packaged *pex* file from `mtvs`_ and put it somewhere on the path like ``/usr/local/bin/``or ``/usr/local/share/bin``or ``~/.local/bin/`` and make it executable,

From this point on, the binary can be executed by calling the *pex* file directly. There exist 3 variants of the *pex* file, depending on the availalbe python version. Choose either *missingTvShows26.pex*, *missingTvShows27.pex* or *missingTvShows35.pex* depending on what is availalbe on your system.

.. only:: builder_html

    Download files directly from here:

    * :download:`missingtvshows_.pex <../dist/missingtvshows_.pex>` For Python > 3.10

From pip
---------

Simply run::

    pipx install missingTvShows


From Sources
-------------

Prepare the environment
^^^^^^^^^^^^^^^^^^^^^^^^

Create a virtual environment and activate it::

    python3 -m venv venv-312
    source venv-312/bin/activate

Define environment variables for compilation if needed (eg. for MySQL support)::

    export GITHUB_API_TOKEN=XXXXXX-XXXX-XXXX-XXXXXXXXXXXX
    export PYPI_API_TOKEN=XXXXXX-XXXX-XXXX-XXXXXXXXXXXX
    export PKG_CONFIG_PATH=$(brew --prefix)/opt/mysql-client/lib/pkgconfig
    export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)
    export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)

Fill an `.envrc` file with these environment variables.


Final installation
^^^^^^^^^^^^^^^^^^

From a terminal launch::

    pip install -r requirements_dev.txt
    pip install .

This will compile and install the project to the Python libraries (eg. ``/usr/local/lib/python3.12/site-packages/missingTvShows-1.2.2.dev51+gf5133b9.d20240930.dist-info``). Furthermore it will install a script in ``/usr/local/bin/``:
* missingtvshows

Upon the first start a copy of a pristine application and logging configuration are created in the user's home directory ``~/.MissingTVShows/``. From this point on configuration files are read from this location. It is however possible to overwrite them either by placing a file with the same name (but prefixed with a dot eg. ``.logging.conf``) in the current working directory.

Development installation
^^^^^^^^^^^^^^^^^^^^^^^^

from a terminal launch::

    pip install -r requirements_dev.txt
    pip install -e .

does the same as before but, uses links instead of copying files. On macOS a few environment variables need to be defined::

    export PKG_CONFIG_PATH=$(brew --prefix)/opt/mysql-client/lib/pkgconfig
    export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)
    export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)

Code Guideline Checking
^^^^^^^^^^^^^^^^^^^^^^^^

To check the code guidelines run::

    flake8 --max-line-length=88 --statistics --extend-ignore=E501,E203,W503 --select=E,W,F .


After fixing the issues you can reformat the code with::

    black .

Run type checks
^^^^^^^^^^^^^^^^^^^^^^

To run type checks on the code base use::

    mypy src tests

All in one command
^^^^^^^^^^^^^^^^^^^^^^

To run code guideline checks and type checks in one command use::

    tox -e lint,type

Clean Working directory
^^^^^^^^^^^^^^^^^^^^^^^^

To clean the working directory::

    python setup.py clean --all
    rm -rf build/ dist/


Release Software
-----------------

Version numbers are derived from the git history with `setuptools_scm <https://github.com/pypa/setuptools-scm>`_: Likely `python -m setuptools_scm` prints the current version. It's a mix from the version of the last git tag plus the `dev` suffix with a number indicating the distance to the last git tag. If the command is called on a commit with a git tag then it just takes that tag.

The releasing itself is done with `twine <https://twine.readthedocs.io/en/latest/index.html>`_

* Build the software: `python -m build` (if not using `tox`) for creating the packages
* Check if everything is ready for deplyoment: `python -m twine check dist/*`
* Upload artifacts: `python -m twine upload --repository pypitest --verbose dist/*`


Uninstall
----------

Method 1 (pip)
^^^^^^^^^^^^^^

If the package was installed with ``pip`` simply run::

    pip uninstall missingTvShows

Method 2 (from sources)
^^^^^^^^^^^^^^^^^^^^^^^

If the packages was installed from sources::

    cat files.txt |sudo xargs rm -rf

Method 3  (from sources)
^^^^^^^^^^^^^^^^^^^^^^^^^

First find the installed package with pip and the uninstall it::

    ✔ ~/Documents/Programming/Python/missingTvShows [master|✚ 1]
    19:02 $ pip3 freeze |grep missingTvShows
    missingTvShows==1.1

    ✔ ~/Documents/Programming/Python/missingTvShows [master|✚ 1]
    19:02 $  pip3 uninstall missingTvShows
    Uninstalling missingTvShows-1.1:
      /usr/local/bin/missingTvShows
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/DESCRIPTION.rst
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/INSTALLER
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/METADATA
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/RECORD
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/WHEEL
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/entry_points.txt
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/metadata.json
      /usr/local/lib/python3.5/site-packages/missingTvShows-1.1.dist-info/top_level.txt
      /usr/local/lib/python3.5/site-packages/missingTvShows/__init__.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/__pycache__/__init__.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/etc/missingTvShows-completion.bash
      /usr/local/lib/python3.5/site-packages/missingTvShows/etc/missingTvShows.conf
      /usr/local/lib/python3.5/site-packages/missingTvShows/etc/logging.conf
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/__init__.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/__pycache__/__init__.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/__pycache__/calendar2itc.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/__pycache__/calendarEvent.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/__pycache__/itcClient.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/calendar2itc.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/calendarEvent.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/itc/itcClient.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/__init__.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/__pycache__/__init__.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/__pycache__/main.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/__pycache__/mainImpl.cpython-35.pyc
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/main.py
      /usr/local/lib/python3.5/site-packages/missingTvShows/main/mainImpl.py
    Proceed (y/n)? y
      Successfully uninstalled missingTvShows-1.1



To install the missingTvShows package, use::

  python setup.py install

If installation is successful, you will be able to import the iCalendar
package, like this::

  >>> import icalendar


Building the documentation locally
----------------------------------

To build the documentation follow these steps:

.. code-block:: bash

    $ git clone http://digsim.is-a-geek.com/rhode/missingTvShows
    $ cd missingTvShows
    $ virtualenv-2.7 .
    $ source bin/activate
    $ pip install -r requirements_docs.txt --extra-index-url http://pypi.is-a-geek.com/simple --trusted-host pypi.is-a-geek.com
    $ cd docs
    $ make html

You can now open the output from ``_build/html/index.html``. To build the
presentation-version use ``make presentation`` instead of ``make html``. You
can open the presentation at ``presentation/index.html``.


.. _`mtvs`: https://www.andreas-ruppen.ch/
