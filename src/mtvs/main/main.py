# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import shutil
import signal
import logging.config
import pkgutil
from importlib.metadata import version
import colorama
import os
from os.path import expanduser

import configparser


class Main(object):
    def __init__(self, configDirName, configName, logFileName):
        """
        Constructor.

        :param configDirName: Name of the directory where the configuration is stored.
        :param configName: Name of the configuration file.
        :param logFileName: Name of the log file.
        """
        colorama.init()
        self.original_sigint = signal.getsignal(signal.SIGINT)
        self.__CONFIG_DIR = pkgutil.get_loader("mtvs").get_filename()
        self.__CONFIG_DIR = os.path.dirname(self.__pathjoin(self.__CONFIG_DIR))
        self.__CONFIG_DIR = self.__pathjoin(self.__CONFIG_DIR, "etc")
        self.__USER_CONFIG_DIR = expanduser("~/." + configDirName)
        self.__configName = configName
        self.__logFileName = logFileName
        self._checkUserConfigFiles()
        self.version = version("mtvs")

        logging.basicConfig(level=logging.DEBUG)
        logging.config.fileConfig(
            [
                self.__pathjoin(self.__CONFIG_DIR, "logging.conf"),
                self.__pathjoin(self.__USER_CONFIG_DIR, "logging.conf"),
                "logging.conf",
            ],
            defaults={
                "logfilename": self.__pathjoin(
                    self.__USER_CONFIG_DIR, self.__logFileName
                )
            },
        )
        self.__log = logging.getLogger("Tube4Droid")

        self.config = configparser.ConfigParser()
        self.config.read(
            [
                self.__pathjoin(self.__CONFIG_DIR, self.__configName),
                self.__pathjoin(self.__USER_CONFIG_DIR, self.__configName),
                self.__configName,
            ]
        )

    def main(self):
        """
        This is the main entry point. Call this function at the end of getArguments

        :return: void
        """
        signal.signal(signal.SIGINT, self._exit_gracefully)
        self.doWork()

    def doWork(self):
        """
        This the main method doing some actual work. This function needs to be overwritten by the <code>mainImpl.py</code> class.

        :return: void
        """
        return

    def getArguments(self, argv):
        """
        Do the argument parsing. This function needs to be overwritten by the <code>mainImpl.py</code> class.

        :param argv: array of command line arguments
        :return: void
        """
        return

    def _checkPythonVersion(self):
        """
        Checks the pyhton version. Does nothing more than log the used version.

        :return: void.
        """
        self.__log.debug("Using Python " + sys.version[:3])

    def _checkUserConfigFiles(self):
        """
        Verifies that the necessary configuration directory and files exist. If not, they are created from skeleton
        files and a message is printed indicating the user that he shall first adapt the default configuration.

        :return: void.
        """
        printWarningAndAbort = False
        if not os.path.exists(self.__CONFIG_DIR):
            print("Could not find initial configuration skeletons. Aborting")
            return
        if not os.path.exists(self.__USER_CONFIG_DIR):
            print("User config dir does not exist. Creating " + self.__USER_CONFIG_DIR)
            os.mkdir(self.__USER_CONFIG_DIR)
            printWarningAndAbort = True
        if not os.path.exists(self.__pathjoin(self.__USER_CONFIG_DIR, "logging.conf")):
            print("Copying default logging conf to " + self.__USER_CONFIG_DIR)
            shutil.copy(
                self.__pathjoin(self.__CONFIG_DIR, "logging.conf"),
                self.__pathjoin(self.__USER_CONFIG_DIR, "logging.conf"),
            )
        if not os.path.exists(
            self.__pathjoin(self.__USER_CONFIG_DIR, self.__configName)
        ):
            print('No application specific config file found. Creating ' + self.__configName + ' in ' + self.__USER_CONFIG_DIR)
            shutil.copy(
                self.__pathjoin(self.__CONFIG_DIR, self.__configName),
                self.__pathjoin(self.__USER_CONFIG_DIR, self.__configName),
            )
            printWarningAndAbort = True
        if printWarningAndAbort:
            print("Created initial configuration files in " + self.__USER_CONFIG_DIR)
            print("Please edit " + self.__USER_CONFIG_DIR + "/" + self.__configName)
            sys.exit(0)

    def _exit_gracefully(self, signum, frame):
        """
        Helper function for signal handling. Responsible for handling CTRL-C and abort the execution.
        Prior to aborting, the user is asked if the really wants to interrupt.

        :param signum:
        :param frame:
        :return: void
        """
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, self.original_sigint)

        real_raw_input = input

        try:
            if real_raw_input("\nReally quit? (y/n)> ").lower().startswith("y"):
                sys.exit(1)
        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)

        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, self._exit_gracefully)

    def __pathjoin(*pathes):
        return os.path.join(*pathes[1:]).replace("\\", "/")
