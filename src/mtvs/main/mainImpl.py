import argparse
import logging
import random
import sys
import time
import typing
from os.path import join

from .main import Main
from mtvs.Kodi.missing_tvshows import TVShows
from mtvs.utils import utilities


class MainImpl(Main):
    def __init__(self) -> None:
        """Constructor"""
        self.__configDirName = "MissingTVShows"
        self.__configName = "tvshows.conf"
        self.__logFileName = "tvshows.log"

        super().__init__(self.__configDirName, self.__configName, self.__logFileName)
        self.__log = logging.getLogger("Tube4Droid")

        self.__command = None
        self.__forceUpdate = False
        self.__forceLocal = False
        self.__produceCVS = False
        self.__totalOfSeriesSeason = 0
        self.__alreadyCheckedSeriesSeason = 0
        self.__random = random.SystemRandom(time.time())
        # Config stuff from config file
        self.__tvdbdatabse = join(
            self.USER_CONFIG_DIR, self.config.get("Config", "tvdbdb")
        )
        self.__api_key = self.config.get("Config", "api_key")
        # Database stuff from config file
        self.__dbdialect = self.config.get("Database", "dialect")
        self.__database = self.config.get("Database", "db")
        self.__dbuser = self.config.get("Database", "user")
        self.__dbpasswd = self.config.get("Database", "passwd")
        self.__dbhostname = self.config.get("Database", "hostname")
        self.__dbport = self.config.get("Database", "port")
        self.__log.debug("Database " + self.__database)

        self.dryrun = False

    def get_arguments(self, argv: list[typing.Any]) -> None:
        """
        Parses the command line arguments.

        :param argv: array of command line arguments
        :return: void
        """
        self._check_python_version()

        parser = argparse.ArgumentParser(
            prog="missingtvshows",
            description="Checks missing TV Show Episodes based on the list of available Episodes on thetvdb.com",
            epilog="%(prog)s {command} -h for help on individual commands",
        )
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + self.version
        )

        subparsers = parser.add_subparsers(help="commands", dest="command")
        sync_parser = subparsers.add_parser("sync", help="sync Kodi and TVDB")

        sync_parser.add_argument(
            "-i",
            "--input",
            help="input sqlite database file",
            required=False,
            metavar="DATABASE",
        )
        sync_parser.add_argument(
            "-f",
            "--force-update",
            help="Force the update of the local TVDB Database",
            required=False,
            action="store_true",
            dest="forceupdate",
        )
        sync_parser.add_argument(
            "-o",
            "--offline",
            help="Force Offline mode, even if the script thinks that some entries needs to be refreshed",
            required=False,
            action="store_true",
            dest="forcelocal",
        )
        sync_parser.add_argument(
            "-c",
            "--csv",
            help="Produce CSV output files",
            required=False,
            action="store_true",
            dest="producecsv",
        )

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        args = parser.parse_args(argv)

        if args.command is not None:
            self.__command = args.command

        if self.__command == "sync":
            self.__database = args.input or self.__database
            self.__forceUpdate = args.forceupdate
            self.__forceLocal = args.forcelocal
            self.__produceCVS = args.producecsv
            if self.__forceLocal:
                self.__forceUpdate = False
            self.main()
        else:
            parser.print_help()
            sys.exit(1)
        sys.exit(0)

    def do_work(self) -> None:
        """
        Overwrites the main

        :return: void
        """
        if self.__command == "sync":
            self.__do_sync_command()

    def __do_sync_command(self) -> None:
        """
        Parses calendar and writes corresponding ITC entries

        :return: void
        """
        tvshows = TVShows(
            self.__tvdbdatabse,
            self.__api_key,
            self.__dbdialect,
            self.__database,
            self.__dbuser,
            self.__dbpasswd,
            self.__dbhostname,
            self.__dbport,
        )
        print("Acquiring necessary TV-Shows information")
        (
            unwatched_finished_shows,
            unwatched_unfinished_shows,
            watchedsome_unfinished_shows,
            watchedsome_finished_shows,
        ) = tvshows.get_series_information()
        utilities.print_konsole(
            unwatched_finished_shows,
            unwatched_unfinished_shows,
            watchedsome_unfinished_shows,
            watchedsome_finished_shows,
        )
        if self.__produceCVS:
            utilities.save_CSV(
                unwatched_finished_shows,
                unwatched_unfinished_shows,
                watchedsome_unfinished_shows,
                watchedsome_finished_shows,
            )


if __name__ == "__main__":
    main = MainImpl()
    main.get_arguments(sys.argv[1:])
