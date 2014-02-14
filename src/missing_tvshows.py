#!/usr/bin/python
# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals
import sqlite3
import sys, os, getopt, shutil
import logging
import logging.config
if float(sys.version[:3])<3.0:
    import ConfigParser
else: 
    import configparser as ConfigParser
import argparse
import time
from pytvdbapi import api
import math
import random


class TVShows:
    def __init__(self):
        """Do some initialization stuff"""
        logging.basicConfig(level=logging.ERROR)
        logging.config.fileConfig('logging.conf')
        self.__log = logging.getLogger('TVShows')
        
        
        # Configure several elements depending on config file
        config = ConfigParser.SafeConfigParser()
        config.read("tvshows.cfg")
        #self.__db = api.TVDB(config.get("Config", "api_key"))
        self.__database = config.get("Config", "db")
        self.__tvdbdatabse = config.get("Config", "tvdbdb")
        self.__cwd = os.getcwd()
        self.__log.debug('Database '+self.__database)
        self.__forceUpdate = False
        self.__totalOfSeriesSeason = 0
        self.__alreadyCheckedSeriesSeason = 0
        self.__random = random.SystemRandom(time.localtime())
        
        self.checkLocalTVDBDatabase()
        
                            
                            
    def make_sql_queries(self):
        con = sqlite3.connect(self.__database)
        cur = con.cursor()
        # Select TV-Shows where no episode has been watched
        cur.execute('select * from (select tvshow.c00 as Title, episodeview.c12 as Season, count(*) as Episodes, tvshow.c12 as SeriesiD, episodeview.idSeason as SeasoniD, max(episodeview.playCount) as Played from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow group by tvshow.c00, episodeview.c12 order by tvshow.c00) where Played is NULL;')
        nonewatched = cur.fetchall()
        
        # Select TV-Shows where at least one Episode was played
        cur.execute('select * from (select tvshow.c00 as Title, episodeview.c12 as Season, count(*) as Episodes, tvshow.c12 as SeriesiD, episodeview.idSeason as SeasoniD, sum(episodeview.playCount) as Played from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow group by tvshow.c00, episodeview.c12 order by tvshow.c00) where Played is not NULL;')
        somewatched = cur.fetchall()
        self.__totalOfSeriesSeason = len(nonewatched) + len(somewatched)
        con.close()
        
        return nonewatched,  somewatched
        
    def getTotalNumberOfEpisodes(self,  series_id,  season):
        con = sqlite3.connect(self.__tvdbdatabse)
        cur = con.cursor()
        cur.execute("Select * from THETVDB where seriesid = {:d} and season = {:d};".format(series_id,  season))
        localshow = cur.fetchone()
        number_of_episodes = 0
        now = time.mktime(time.localtime())
        self.__alreadyCheckedSeriesSeason = self.__alreadyCheckedSeriesSeason+1
        progress = self.__alreadyCheckedSeriesSeason*100/self.__totalOfSeriesSeason
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('='*int(math.ceil(progress)), progress ))
        sys.stdout.flush()
        self.__log.debug("Already done {:d} of {:d}".format(self.__alreadyCheckedSeriesSeason,  self.__totalOfSeriesSeason))
        if not localshow and not self.__forceLocal:
            show = self.__db.get(series_id, "en" )
            number_of_episodes = len(show[season])
            next_update_time = now + self.__random.randint(0,  302400)
            self.__log.debug('Next update time is: '+str(next_update_time))
            cur = con.cursor()
            cur.execute('''INSERT INTO THETVDB VALUES (NULL, {:d}, {:d}, {:d}, {:f})'''.format(series_id,  season,  number_of_episodes,  next_update_time ))
            con.commit()
        elif not localshow and self.__forceLocal:
            number_of_episodes = -1
        elif self.__forceUpdate or ((now-localshow[4] > 604800) and not self.__forceLocal):
            show = self.__db.get(series_id, "en" )
            number_of_episodes = len(show[season])
            cur = con.cursor()
            next_update_time = now + self.__random.randint(0,  302400)
            self.__log.debug('Next update time is: '+str(next_update_time))
            cur.execute('''UPDATE THETVDB SET totalnumofepisodes={:d},  lastupdated={:f} where id = {:d}'''.format(number_of_episodes,  next_update_time,  localshow[0]))
            con.commit()
        else:
            number_of_episodes = localshow[3]
            
        con.close()
        return number_of_episodes
        
    def checkLocalTVDBDatabase(self):
        con = sqlite3.connect(self.__tvdbdatabse)
        cur = con.cursor()
        cur.execute("Select name from sqlite_master where type='table';")
        if not cur.fetchall():
            cur = con.cursor()
            cur.execute('''CREATE TABLE THETVDB (id INTEGER PRIMARY KEY, seriesid INTEGER, season INTEGER, totalnumofepisodes INTEGER, lastupdated REAL)''')
            con.commit()
        con.close()
        
    def checkXBMCDatabase(self):
        try:
            with open(self.__database):
                pass
        except IOError:
            self.__log.error('XBMC Database not found - Aborting')
            sys.exit(-404)
   
        
    def getSeriesInformation(self):
        """The main function"""
        if not self.__forceLocal:
            self.__db = api.TVDB(config.get("Config", "api_key"))
        nonewatched,  somewatched = self.make_sql_queries()
        con = sqlite3.connect(self.__database)
        cur = con.cursor()
        
        unwatched_finished_shows = []
        unwatched_unfinished_shows =  []
        watchedsome_unfinished_shows = []
        watchedsome_finished_shows = []
        

        for row in nonewatched:
            if(int(row[1]) == 0): # Don't take into consideration Season 0
                continue
            rowTitle = row[0]#.encode('utf-8')
            rowId = row[3]
            rowSeason = row[1]
            rowDownloaded = row[2]
            self.__log.debug('Currently treating series {:s} with id: {:s} and Season {:s}'.format(rowTitle,  rowId,  rowSeason))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(rowId),  int(rowSeason))
            full_episodes = range(1, number_of_episodes+1)
            self.__log.debug('{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes'.format( rowTitle,  rowSeason,  rowDownloaded,  number_of_episodes))
            
            if(int(number_of_episodes) != int(rowDownloaded)): # If number of local Episodes is different from TheTVDB
                # Select all availalbe Episodes of current Series and Season
                cur.execute('select tvshow.c00 as Title, episodeview.c12 as Season, episodeview.c13 as Episode, tvshow.c12 as SeriesiD  from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow where Season={:s} and SeriesiD={:s}  order by tvshow.c00, episodeview.c12, episodeview.c13;'.format(rowSeason,  rowId))
                episodes = cur.fetchall()
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])
                present_episodes = map(int,  present_episodes)
                self.__log.debug('Present episodes '+str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug('Missing episodes: '+str(missing_episodes)[1:-1])
                unwatched_unfinished_shows.append({'Title':rowTitle,  'SeasonId':rowId,  'Season':rowSeason,  'NbDownloaded':rowDownloaded,  'NbAvailable':number_of_episodes, 'NbWatched':0,   'MissingEpisodes':str(missing_episodes)[1:-1]})
            else:
                unwatched_finished_shows.append({'Title':rowTitle,  'SeasonId':rowId,  'Season':rowSeason,  'NbDownloaded':rowDownloaded,  'NbAvailable':number_of_episodes, 'NbWatched':0,  'MissingEpisodes':0})
                

        
        for row in somewatched:
            if(int(row[1]) == 0): # Don't take into consideration Season 0
                continue
            rowTitle = row[0]#.encode('utf-8')
            rowId = row[3]
            rowSeason = row[1]
            rowDownloaded = row[2]
            rowWatched = row[5]
            self.__log.debug('Currently treating series {:s} with id: {:s} and Season {:s}'.format(rowTitle,  rowId,  rowSeason))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(rowId),  int(rowSeason))
            full_episodes = range(1, number_of_episodes+1)
            if(int(number_of_episodes) != int(rowDownloaded)): # If number of local Episodes is different from TheTVDB
                cur.execute('select tvshow.c00 as Title, episodeview.c12 as Season, episodeview.c13 as Episode, tvshow.c12 as SeriesiD  from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow where Season={:s} and SeriesiD={:s}  order by tvshow.c00, episodeview.c12, episodeview.c13;'.format(rowSeason,  rowId))
                episodes = cur.fetchall()
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])
                present_episodes = map(int,  present_episodes)
                self.__log.debug('Present episodes: '+str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug('Missing episodes: '+str(missing_episodes)[1:-1])
                watchedsome_unfinished_shows.append({'Title':rowTitle,  'SeasonId':rowId,  'Season':rowSeason,  'NbDownloaded':rowDownloaded,  'NbAvailable':number_of_episodes, 'NbWatched':rowWatched,  'MissingEpisodes':str(missing_episodes)[1:-1]})
            elif int(number_of_episodes) > rowWatched:
                watchedsome_finished_shows.append({'Title':rowTitle,  'SeasonId':rowId,  'Season':rowSeason,  'NbDownloaded':rowDownloaded,  'NbAvailable':number_of_episodes,  'NbWatched':rowWatched, 'MissingEpisodes':0})
        con.close()
        return unwatched_finished_shows,  unwatched_unfinished_shows,  watchedsome_unfinished_shows,  watchedsome_finished_shows
        
        
            
    def main(self):
        print('Acquiring necessary TV-Shows information')
        unwatched_finished_shows,  unwatched_unfinished_shows,  watchedsome_unfinished_shows,  watchedsome_finished_shows = self.getSeriesInformation()
        sys.stdout.write('\n')
        print('##############################################################')
        print('###################### Unwatched Missing #####################')
        print('##############################################################')
        
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        print('|{:44s} | {:s} ({:s}/{:s})| {:74s}|'.format('Title', 'Season', 'Downloaded',  'Available',  'Missing'))
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        for row in unwatched_unfinished_shows:
            print('|{:43s}: | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row['Title'], row['Season'], row['NbDownloaded'],  row['NbAvailable'],  row['MissingEpisodes']))
            print('-------------------------------------------------------------------------------------------------------------------------------------------------')
            
        print('###############################################################')
        print('######################## Watched Missing ######################')
        print('###############################################################')
        
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        print('|{:35s}({:8s})  | {:s} ({:s}/{:s})| {:74s}|'.format('Title', 'SeasonId', 'Season', 'Downloaded',  'Available',  'Missing'))
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        for row in watchedsome_unfinished_shows:
            print('|{:35s}({:8s}): | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row['Title'], row['SeasonId'], row['Season'], row['NbDownloaded'],  row['NbAvailable'],  row['MissingEpisodes']))
            print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        
        print('###############################################################')
        print('######################## Ready to Watch #######################')
        print('###############################################################')
        for row in unwatched_finished_shows:
            print('{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes'.format( row['Title'], row['Season'], row['NbDownloaded'], row['NbAvailable']))
            
        print('###############################################################')
        print('#################### Complete and Watching ####################')
        print('###############################################################')
        for row in watchedsome_finished_shows:
            print('{:35s}: Season {:2s} and has watched {:2d}/{:2d} Episodes'.format(  row['Title'], row['Season'], row['NbWatched'], row['NbDownloaded']))
            
        
    def getArguments(self, argv):
        parser = argparse.ArgumentParser(prog='missing_tvshows',  description='Parsing the local XBMC library for TV-Shows and discovers if new episodes are availalbe',  epilog='And that is how you use me')
        parser.add_argument("-i",  "--input",  help="input sqlite database file",  required=False,  metavar='DATABASE')
        parser.add_argument("-f",  "--force-update",  help="Force the update of the local TVDB Database",  required=False,  action="store_true",  dest='forceupdate')
        parser.add_argument("-o",  "--offline",  help="Force Offline mode, even if the script thinks that some entries needs to be refreshed",  required=False,  action="store_true",  dest='forcelocal')
        args = parser.parse_args(argv)
        self.__database = args.input or self.__database
        self.__forceUpdate = args.forceupdate
        self.__forceLocal = args.forcelocal
        if self.__forceLocal:
            self.__forceUpdate = False
        self.checkXBMCDatabase()
        self.main()
        
        
if __name__ == "__main__":
    sms = TVShows()
    sms.getArguments(sys.argv[1:])
