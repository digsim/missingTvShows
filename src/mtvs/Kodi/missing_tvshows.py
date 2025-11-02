#!/usr/bin/python
#########################################################################
# Simple script which is parsing all TV-Shows in the local XBMC MyVideos75.db                                                              #
# For each TV-Show and for each Season TheTVDB is asked to know how many Episodes exists in this Season.              #
# The returned value from TheTVDB is then compared to the locally availalbe Episodes.                                                  #
# Finally 4 lists are printed:                                                                                                                                                  #
#       Seasons where no Episode is watched and which is not yet complete                                                                        #
#       Seasons where some Episodes are watched but the Season is not yet complete                                                        #
#       Seasons where no Episode is watched and all Episodes are locally available                                                             #
#       Seasons where some Episodes are watched and all Episodes are locally availalbe                                                    #
# For the Seasons having missing Episodes, the script prints an array containing the Episodes numbers                         #
# of the missing Episodes.                                                                                                                                                     #
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                                             #
# Author: Andreas Ruppen                                                                                                                                                     #
# Copyright 2013 Andreas Ruppen                                                                                                                                        #
# Licensed under the Apache License, Version 2.0 (the "License");                                                                                      #
#   you may not use this file except in compliance with the License.                                                                                    #
#   You may obtain a copy of the License at                                                                                                                           #
#                                                                                                                                                                                              #
#       http://www.apache.org/licenses/LICENSE-2.0                                                                                                               #
#                                                                                                                                                                                              #
#   Unless required by applicable law or agreed to in writing, software                                                                                #
#   distributed under the License is distributed on an "AS IS" BASIS,                                                                                   #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                                   #
#   See the License for the specific language governing permissions and                                                                             #
#   limitations under the License.                                                                                                                                            #
###########################################################################
import logging.config
import math
import os
import random
import sqlite3
import sys
import time
import typing

import tvdb_v4_official  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists  # type: ignore

import mtvs._types


class TVShows:
    def __init__(
        self,
        tvdbdatabase: str,
        apikey: str,
        dbdialect: str,
        database: str,
        dbuser: str,
        dbpasswd: str,
        dbhost: str,
        dbport: str,
    ) -> None:
        """Do some initialization stuff"""

        self.__log = logging.getLogger("Tube4Droid")
        self.__forceUpdate = False
        self.__forceLocal = False
        self.__produceCVS = False
        self.__totalOfSeriesSeason = 0
        self.__alreadyCheckedSeriesSeason = 0
        self.__random = random.SystemRandom(time.time())
        # Config stuff from config file
        self.__tvdbdatabse = tvdbdatabase
        self.__api_key = apikey
        # Database stuff from config file
        self.__dbdialect = dbdialect
        self.__database = database
        self.__dbuser = dbuser
        self.__dbpasswd = dbpasswd
        self.__dbhostname = dbhost
        self.__dbport = dbport
        self.__log.debug("Database " + self.__database)

        self._check_local_tvdb_database()

    def _check_local_tvdb_database(self) -> None:
        """
        Checks if the local thetvdb.com cache DB is initialized. In order to save bandwith and not hit to badly thetvdb.com
        the results stay cached for approx. 7 days. This function checks if this cache Sqlite DB exists and if not
        initializes the DB.

        :return: Nothing
        """
        con = sqlite3.connect(self.__tvdbdatabse)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if not cur.fetchall():
            cur = con.cursor()
            cur.execute(
                """CREATE TABLE THETVDB (id INTEGER PRIMARY KEY, seriesid INTEGER, season INTEGER, totalnumofepisodes INTEGER, lastupdated REAL)"""
            )
            con.commit()
        con.close()

    def _init_db_connection(self) -> None:
        """
        Initializes the DB connections to Kodi's database. This connection can either be an MySQL or an Sqlite connection.
        Furthermore, this functions defines some Kodi tables which will later be used in various queries.

        :return: Nothing
        """
        db_connection_string = ""
        try:
            if self.__dbdialect == "mysql":
                db_connection_string = (
                    "mysql://"
                    + self.__dbuser
                    + ":"
                    + self.__dbpasswd
                    + "@"
                    + self.__dbhostname
                    + ":"
                    + self.__dbport
                    + "/"
                    + self.__database
                )
            elif self.__dbdialect == "sqlite":
                db_connection_string = "sqlite:///" + self.__database
                if not self._is_sqlite3(self.__database):
                    raise ValueError(
                        self.__database + " is not a valid sqlite database"
                    )

            if not database_exists(db_connection_string):
                raise ValueError("Database does not exist")
            engine = create_engine(db_connection_string)

            self.__log.debug("Connected to database " + self.__database)

        except ProgrammingError:
            self.__log.error("Connection to database " + self.__database + " failed")
            raise ValueError("Could not connect to " + db_connection_string)

        session = sessionmaker(bind=engine)
        self.__session = session()
        metaData = MetaData()
        metaData.reflect(engine)

        # Map XBMC tables to objects
        self.__tvshow = Table("tvshow", metaData, autoload_with=engine)
        self.__seasons = Table("seasons", metaData, autoload_with=engine)
        self.__episodeview = Table("episode_view", metaData, autoload_with=engine)
        self.__uniqueid = Table("uniqueid", metaData, autoload_with=engine)

    def _is_sqlite3(self, filename: str | os.PathLike) -> bool:
        """
        Checks if a file is an Sqlite DB.
        Courtesy of http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists.

        :param filename: Location of sqlite db.
        :return: true if an sqlite db is found, false otherwise.
        """
        from os.path import isfile, getsize

        if not isfile(filename):
            return False
        if getsize(filename) < 100:  # SQLite database file header is 100 bytes
            return False

        with open(filename, "rb") as f:
            header = f.read(100)

        return header[0:16] == b"SQLite format 3\000"

    def _make_sql_queries(self) -> tuple[list[typing.Any], list[typing.Any]]:
        """
        Queries the Kodi database for availalbe series. Two queries are made, the first one queries all tv shows where
        no episode is watched so far. These series will be candidates for the sections 'Ready to Watch' and 'Unwatched Missing'.
        The second, queries all tv shows having at least one watched episodes. These series will be candidates for
        'Watched missing' and 'Complete and Watching'.
        If more than one season is available for a given series, it will occur multiple times in either one or the other
        or both lists.

        :return: two list of locally availalbe series.
        """
        self._init_db_connection()
        session = self.__session
        tvshow = self.__tvshow
        seasons = self.__seasons
        episodeview = self.__episodeview
        uniqueid = self.__uniqueid

        query = (
            session.query(
                tvshow.c.c00.label("Title"),
                episodeview.c.c12.label("Season"),
                func.count().label("Episodes"),
                uniqueid.c.value.label("SeriesID"),
                episodeview.c.idSeason.label("SeasoniD"),
                func.sum(episodeview.c.playCount).label("Played"),
            )
            .select_from(
                episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason)
                .join(tvshow, tvshow.c.idShow == seasons.c.idShow)
                .join(uniqueid, uniqueid.c.uniqueid_id == tvshow.c.c12)
            )
            .group_by("Title", "Season")
            .order_by("Title")
            .having(func.sum(episodeview.c.playCount) == None)  # noqa: E711
        )

        nonewatched = query.all()

        query = (
            session.query(
                tvshow.c.c00.label("Title"),
                episodeview.c.c12.label("Season"),
                func.count().label("Episodes"),
                uniqueid.c.value.label("SeriesID"),
                episodeview.c.idSeason.label("SeasoniD"),
                func.sum(episodeview.c.playCount).label("Played"),
            )
            .select_from(
                episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason)
                .join(tvshow, tvshow.c.idShow == seasons.c.idShow)
                .join(uniqueid, uniqueid.c.uniqueid_id == tvshow.c.c12)
            )
            .group_by("Title", "Season")
            .order_by("Title")
            .having(func.sum(episodeview.c.playCount) > 0)
        )
        self.__log.debug(str(query.statement.compile()))
        somewatched = query.all()

        self.__totalOfSeriesSeason = len(nonewatched) + len(somewatched)
        return nonewatched, somewatched

    def _get_episodes(
        self, season: int, seriesId: int
    ) -> list[tuple[str, str, str, str]]:
        """
        Queries the episodes of a given serie and a given season.

        :param season: Season to check
        :param seriesId: Serie to check. The id corresponds to the thetvdb.com id.
        :return: a list of locally availalbe episodes.
        """

        session = self.__session
        tvshow = self.__tvshow
        seasons = self.__seasons
        episodeview = self.__episodeview
        uniqueid = self.__uniqueid

        query = (
            session.query(
                tvshow.c.c00.label("Title"),
                episodeview.c.c12.label("Season"),
                episodeview.c.c13.label("Episode"),
                uniqueid.c.value.label("SeriesID"),
            )
            .select_from(
                episodeview.join(seasons, seasons.c.idSeason == episodeview.c.idSeason)
                .join(tvshow, tvshow.c.idShow == seasons.c.idShow)
                .join(uniqueid, uniqueid.c.uniqueid_id == tvshow.c.c12)
            )
            .filter(episodeview.c.c12 == season, uniqueid.c.value == seriesId)
            .order_by("Title", "Season", "Episode")
        )

        episodes: list[tuple[str, str, str, str]] = query.all()
        return episodes

    def get_total_number_of_episodes(self, series_id: int, season: int) -> int:
        """
        Queries to number of aired episodes according to thetvdb.com. To save bandwith, we first check in the local
        thetvdb cache which is stored in a Sqlite DB. If we have a cache miss, we query thetvdb directly and store
        the result in the local SQlite DB.

        :param series_id: Series to look-up. Corresponds to the thetvdb.com identifier.
        :param season: Season to look-up.
        :return: the number of aired episodes.
        """
        self.__log.debug(
            "getTotalNumberOfEpisodes: series_id: {:d} season: {:d}".format(
                series_id, season
            )
        )
        engine = create_engine("sqlite:///" + self.__tvdbdatabse)
        sessionma = sessionmaker(bind=engine)
        session = sessionma()

        query = (
            session.query(TVShow).filter_by(seriesid=series_id).filter_by(season=season)
        )
        localshow: TVShow | None = query.first()

        if localshow is None:
            self.__log.debug(
                "No local cache entry found for series_id: {:d} season: {:d}".format(
                    series_id, season
                )
            )
            return -1

        number_of_episodes = 0
        now = time.mktime(time.localtime())
        self.__alreadyCheckedSeriesSeason += 1
        progress = self.__alreadyCheckedSeriesSeason * 100 / self.__totalOfSeriesSeason
        sys.stdout.write("\r")
        sys.stdout.write("[%-100s] %d%%" % ("=" * int(math.ceil(progress)), progress))
        sys.stdout.flush()
        self.__log.debug(
            "Already done {:d} of {:d}".format(
                self.__alreadyCheckedSeriesSeason, self.__totalOfSeriesSeason
            )
        )
        if not localshow and not self.__forceLocal:
            season_type = "default"
            page = 0
            lang = None
            url = self.__db.url.construct(
                "series",
                series_id,
                "episodes/" + season_type,
                lang,
                page=page,
                season=season,
            )
            episodes = self.__db.request.make_request(url, None)
            number_of_episodes = len(episodes["episodes"])
            next_update_time = now + self.__random.randint(0, 302400)
            self.__log.debug("Next update time is: " + str(next_update_time))
            newlocalshow = TVShow(
                seriesid=series_id,
                season=season,
                totalnumofepisodes=number_of_episodes,
                lastupdated=next_update_time,
            )
            session.add(newlocalshow)
            session.commit()
        elif not localshow and self.__forceLocal:
            number_of_episodes = -1
        elif self.__forceUpdate or (
            (now - float(localshow.lastupdated) > 604800) and not self.__forceLocal
        ):
            season_type = "default"
            page = 0
            lang = None
            url = self.__db.url.construct(
                "series",
                series_id,
                "episodes/" + season_type,
                lang,
                page=page,
                season=season,
            )
            episodes = self.__db.request.make_request(url, None)
            number_of_episodes = len(episodes["episodes"])
            next_update_time = now + self.__random.randint(0, 302400)
            self.__log.debug("Next update time is: " + str(next_update_time))
            localshow.totalnumofepisodes = number_of_episodes
            localshow.lastupdated = next_update_time  # type: ignore
            session.commit()
        else:
            number_of_episodes = localshow.totalnumofepisodes

        session.close()
        return number_of_episodes

    def get_series_information(
        self,
    ) -> tuple[
        list[mtvs._types.MtvsTvShow],
        list[mtvs._types.MtvsTvShow],
        list[mtvs._types.MtvsTvShow],
        list[mtvs._types.MtvsTvShow],
    ]:
        """
        Main function. Puts all pieces together. It queries the local Kodi DB and compares the locally availalbe
        episodes for each Serie/Season combinaton and compares these results with the avialable episodes on
        thetvdb.com

        :return: Nothing
        """

        if not self.__forceLocal:
            self.__db = tvdb_v4_official.TVDB(self.__api_key)
        try:
            nonewatched, somewatched = self._make_sql_queries()
        except ValueError as ve:
            self.__log.error(f"Could not query database: {str(ve)}")
            sys.exit(-5)

        unwatched_finished_shows: list[mtvs._types.MtvsTvShow] = []
        unwatched_unfinished_shows: list[mtvs._types.MtvsTvShow] = []
        watchedsome_unfinished_shows: list[mtvs._types.MtvsTvShow] = []
        watchedsome_finished_shows: list[mtvs._types.MtvsTvShow] = []

        for row in nonewatched:
            if int(row[1]) == 0:  # Don't take into consideration Season 0
                continue
            rowTitle: str = row[0]  # .encode('utf-8')
            rowId: int = row[3]
            rowSeason: int = row[1]
            rowDownloaded: int = row[2]
            self.__log.debug(
                "Currently treating series {:s} with id: {:s} and Season {:s}".format(
                    rowTitle, rowId, rowSeason
                )
            )
            number_of_episodes = self.get_total_number_of_episodes(
                int(rowId), int(rowSeason)
            )
            full_episodes = range(1, number_of_episodes + 1)
            self.__log.debug(
                "{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes".format(
                    rowTitle, rowSeason, rowDownloaded, number_of_episodes
                )
            )

            if int(number_of_episodes) != int(
                rowDownloaded
            ):  # If number of local Episodes is different from TheTVDB
                # Select all availalbe Episodes of current Series and Season
                episodes = self._get_episodes(rowSeason, rowId)
                present_episodes: list[int] = []
                for episode in episodes:
                    present_episodes.append(int(episode[2]))
                self.__log.debug("Present episodes " + str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug("Missing episodes: " + str(missing_episodes)[1:-1])
                unwatched_unfinished_shows.append(
                    {
                        "Title": rowTitle,
                        "SeasonId": rowId,
                        "Season": rowSeason,
                        "NbDownloaded": rowDownloaded,
                        "NbAvailable": number_of_episodes,
                        "NbWatched": 0,
                        "MissingEpisodes": str(missing_episodes)[1:-1],
                    }
                )
            else:
                unwatched_finished_shows.append(
                    {
                        "Title": rowTitle,
                        "SeasonId": rowId,
                        "Season": rowSeason,
                        "NbDownloaded": rowDownloaded,
                        "NbAvailable": number_of_episodes,
                        "NbWatched": 0,
                        "MissingEpisodes": "0",
                    }
                )

        for row in somewatched:
            if int(row[1]) == 0:  # Don't take into consideration Season 0
                continue
            rowTitle = row[0]  # .encode('utf-8')
            rowId = row[3]
            rowSeason = row[1]
            rowDownloaded = row[2]
            rowWatched = row[5]
            self.__log.debug(
                "Currently treating series {:s} with id: {:s} and Season {:s}".format(
                    rowTitle, rowId, rowSeason
                )
            )
            number_of_episodes = self.get_total_number_of_episodes(
                int(rowId), int(rowSeason)
            )
            full_episodes = range(1, number_of_episodes + 1)
            if int(number_of_episodes) != int(
                rowDownloaded
            ):  # If number of local Episodes is different from TheTVDB
                # Select all availalbe Episodes of current Series and Season
                episodes = self._get_episodes(rowSeason, rowId)
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(int(episode[2]))
                self.__log.debug("Present episodes: " + str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug("Missing episodes: " + str(missing_episodes)[1:-1])
                watchedsome_unfinished_shows.append(
                    {
                        "Title": rowTitle,
                        "SeasonId": rowId,
                        "Season": rowSeason,
                        "NbDownloaded": rowDownloaded,
                        "NbAvailable": number_of_episodes,
                        "NbWatched": rowWatched,
                        "MissingEpisodes": str(missing_episodes)[1:-1],
                    }
                )
            elif int(number_of_episodes) > rowWatched:
                watchedsome_finished_shows.append(
                    {
                        "Title": rowTitle,
                        "SeasonId": rowId,
                        "Season": rowSeason,
                        "NbDownloaded": rowDownloaded,
                        "NbAvailable": number_of_episodes,
                        "NbWatched": rowWatched,
                        "MissingEpisodes": "0",
                    }
                )
        return (
            unwatched_finished_shows,
            unwatched_unfinished_shows,
            watchedsome_unfinished_shows,
            watchedsome_finished_shows,
        )


#################################################
# Class representing one TVShow stored in
# the local TVDB cache DB
#################################################
# declarative base class
class Base(DeclarativeBase):
    pass


class TVShow(Base):
    __tablename__ = "THETVDB"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="ignore_fk"
    )
    seriesid: Mapped[int] = mapped_column(Integer)
    season: Mapped[int] = mapped_column(Integer)
    totalnumofepisodes: Mapped[int] = mapped_column(Integer)
    lastupdated: Mapped[float] = mapped_column(Float)


if __name__ == "__main__":
    sms = TVShows("./tvdbdb.db", "api-key", "sqlite", "/test.db", "", "", "", "")
