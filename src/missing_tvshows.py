#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################################################################
# This script is a simple management system for series made of exercises and solution.                                                                                                                                                    #
# It is possible to make zipped series for moodle, a zip containing all series. Furthermore one can                                                                                                                                   #
# generate previews for one exercise/solution. Two handy functions are the make-workbook and the                                                                                                                               #
# make-catalogue. The former one creaets a pdf containig all series, each one followed by its solution                                                                                                                             #
# just like they were distributed. The latter one create a sort of index of all available exercises in                                                                                                                                    #
# the system. Each exercise is followed by its solution.                                                                                                                                                                                                        #
#                                                                                                                                                                                                                                                                                             #
# The structure for a new exercise should be created by using the make-new-exercise function.                                                                                                                                       #
# For further help, please refer to the help function of the software.                                                                                                                                                                                   #
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                                                                                                                                             #
# Author: Andreas Ruppen                                                                                                                                                                                                                                                    #
# License: GPL                                                                                                                                                                                                                                                                       #
# This program is free software; you can redistribute it and/or modify                                                                                                                                                                                 #
#   it under the terms of the GNU General Public License as published by                                                                                                                                                                            #
#   the Free Software Foundation; either version 2 of the License, or                                                                                                                                                                                    #
#   (at your option) any later version.                                                                                                                                                                                                                                      #
#                                                                                                                                                                                                                                                                                               #
#   This program is distributed in the hope that it will be useful,                                                                                                                                                                                            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of                                                                                                                                                                            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                                                                                                                                     #
#   GNU General Public License for more details.                                                                                                                                                                                                                   #
#                                                                                                                                                                                                                                                                                                #
#   You should have received a copy of the GNU General Public License                                                                                                                                                                                 #
#   along with this program; if not, write to the                                                                                                                                                                                                                         #
#   Free Software Foundation, Inc.,                                                                                                                                                                                                                                           #
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.                                                                                                                                                                                              #
################################################################################################################

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

class TVShows:
    def __init__(self):
        """Do some initialization stuff"""
        logging.basicConfig(level=logging.ERROR)
        logging.config.fileConfig('logging.conf')
        self.__log = logging.getLogger('TVShows')
        
        
        # Configure several elements depending on config file
        config = ConfigParser.SafeConfigParser()
        config.read("tvshows.cfg")
        self.__db = api.TVDB(config.get("Config", "api_key"))
        self.__database = config.get("Config", "db")
        self.__tvdbdatabse = config.get("Config", "tvdbdb")
        self.__cwd = os.getcwd()
        self.__log.debug('Database '+self.__database)
        self.__forceUpdate = False
        
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
        con.close()
        
        return nonewatched,  somewatched
        
    def getTotalNumberOfEpisodes(self,  series_id,  season):
        con = sqlite3.connect(self.__tvdbdatabse)
        cur = con.cursor()
        cur.execute("Select * from THETVDB where seriesid = {:d} and season = {:d};".format(series_id,  season))
        localshow = cur.fetchone()
        number_of_episodes = 0
        now = time.mktime(time.gmtime())
        if not localshow or self.__forceUpdate:
            show = self.__db.get(series_id, "en" )
            number_of_episodes = len(show[season])
            cur = con.cursor()
            cur.execute('''INSERT INTO THETVDB VALUES (NULL, {:d}, {:d}, {:d}, {:f})'''.format(series_id,  season,  number_of_episodes,  now ))
            con.commit()
        elif self.__forceUpdate or (now-localshow[4] > 604800):
            show = self.__db.get(series_id, "en" )
            number_of_episodes = len(show[season])
            cur = con.cursor()
            cur.execute('''UPDATE THETVDB SET totalnumofepisodes={:d},  lastupdated={:f} where id = {:d}'''.format(number_of_episodes,  now,  localshow[0]))
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
            self.__log.debug('Currently treating series {:s} with id: {:s} and Season {:s}'.format(row[0],  row[3],  row[1]))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(row[3]),  int(row[1]))
            full_episodes = range(1, number_of_episodes+1)
            self.__log.debug('{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes'.format( row[0],  row[1],  row[2],  number_of_episodes))
            
            if(int(number_of_episodes) != int(row[2])): # If number of local Episodes is different from TheTVDB
                # Select all availalbe Episodes of current Series and Season
                cur.execute('select tvshow.c00 as Title, episodeview.c12 as Season, episodeview.c13 as Episode, tvshow.c12 as SeriesiD  from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow where Season={:s} and SeriesiD={:s}  order by tvshow.c00, episodeview.c12, episodeview.c13;'.format(row[1],  row[3]))
                episodes = cur.fetchall()
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])
                present_episodes = map(int,  present_episodes)
                self.__log.debug('Present episodes '+str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug('Missing episodes: '+str(missing_episodes)[1:-1])
                #unwatched_unfinished_shows.append('|{:43s}: | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row[0],  row[1], row[2],  number_of_episodes,  str(missing_episodes)[1:-1]))
                unwatched_unfinished_shows.append({'Title':row[0],  'SeasonId':row[3],  'Season':row[1],  'NbDownloaded':row[2],  'NbAvailable':number_of_episodes, 'NbWatched':0,   'MissingEpisodes':str(missing_episodes)[1:-1]})
            else:
                #unwatched_finished_shows.append('{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes'.format( row[0],  row[1],  row[2],  number_of_episodes))
                unwatched_finished_shows.append({'Title':row[0],  'SeasonId':row[3],  'Season':row[1],  'NbDownloaded':row[2],  'NbAvailable':number_of_episodes, 'NbWatched':0,  'MissingEpisodes':0})
                

        
        for row in somewatched:
            if(int(row[1]) == 0): # Don't take into consideration Season 0
                continue
            self.__log.debug('Currently treating series {:s} with id: {:s} and Season {:s}'.format(row[0],  row[3],  row[1]))
            number_of_episodes = self.getTotalNumberOfEpisodes(int(row[3]),  int(row[1]))
            full_episodes = range(1, number_of_episodes+1)
            if(int(number_of_episodes) != int(row[2])): # If number of local Episodes is different from TheTVDB
                cur.execute('select tvshow.c00 as Title, episodeview.c12 as Season, episodeview.c13 as Episode, tvshow.c12 as SeriesiD  from episodeview join seasons on seasons.idSeason = episodeview.idSeason join tvshow on tvshow.idShow = seasons.idShow where Season={:s} and SeriesiD={:s}  order by tvshow.c00, episodeview.c12, episodeview.c13;'.format(row[1],  row[3]))
                episodes = cur.fetchall()
                present_episodes = []
                for episode in episodes:
                    present_episodes.append(episode[2])
                present_episodes = map(int,  present_episodes)
                self.__log.debug('Present episodes: '+str(present_episodes))
                missing_episodes = list(set(full_episodes) - set(present_episodes))
                self.__log.debug('Missing episodes: '+str(missing_episodes)[1:-1])
                #watchedsome_unfinished_shows.append('|{:35s}({:8s}): | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row[0], row[3], row[1], row[2],  number_of_episodes,  str(missing_episodes)[1:-1]))
                watchedsome_unfinished_shows.append({'Title':row[0],  'SeasonId':row[3],  'Season':row[1],  'NbDownloaded':row[2],  'NbAvailable':number_of_episodes, 'NbWatched':row[5],  'MissingEpisodes':str(missing_episodes)[1:-1]})
            elif int(number_of_episodes) > row[5]:
                #watchedsome_finished_shows.append('{:35s}: Season {:2s} and has watched {:2d}/{:2d} Episodes'.format( row[0],  row[1],  row[5],  number_of_episodes))
                watchedsome_finished_shows.append({'Title':row[0],  'SeasonId':row[3],  'Season':row[1],  'NbDownloaded':row[2],  'NbAvailable':number_of_episodes,  'NbWatched':row[5], 'MissingEpisodes':0})
        con.close()
        return unwatched_finished_shows,  unwatched_unfinished_shows,  watchedsome_unfinished_shows,  watchedsome_finished_shows
        
        
            
    def main(self):
        unwatched_finished_shows,  unwatched_unfinished_shows,  watchedsome_unfinished_shows,  watchedsome_finished_shows = self.getSeriesInformation()
        print('##############################################################')
        print('###################### Unwatched Missing #####################')
        print('##############################################################')
        
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        print('|{:44s} | {:s} ({:s}/{:s})| {:74s}|'.format('Title', 'Season', 'Downloaded',  'Available',  'Missing'))
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        for row in unwatched_unfinished_shows:
            print('|{:43s}: | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row['Title'],  row['Season'], row['NbDownloaded'],  row['NbAvailable'],  row['MissingEpisodes']))
            print('-------------------------------------------------------------------------------------------------------------------------------------------------')
            
        print('###############################################################')
        print('######################## Watched Missing ######################')
        print('###############################################################')
        
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        print('|{:35s}({:8s})  | {:s} ({:s}/{:s})| {:74s}|'.format('Title', 'SeasonId', 'Season', 'Downloaded',  'Available',  'Missing'))
        print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        for row in watchedsome_unfinished_shows:
            print('|{:35s}({:8s}): | S{:2s} ({:2d}/{:2d})| missing: {:74s}|'.format(row['Title'], row['SeasonId'],   row['Season'], row['NbDownloaded'],  row['NbAvailable'],  row['MissingEpisodes']))
            print('-------------------------------------------------------------------------------------------------------------------------------------------------')
        
        print('###############################################################')
        print('######################## Ready to Watch #######################')
        print('###############################################################')
        for row in unwatched_finished_shows:
            print('{:35s}: Season {:2s} and has {:2d}/{:2d} Episodes'.format( row['Title'],  row['Season'],  row['NbDownloaded'], row['NbAvailable']))
            
        print('###############################################################')
        print('#################### Complete and Watching ####################')
        print('###############################################################')
        for row in watchedsome_finished_shows:
            print('{:35s}: Season {:2s} and has watched {:2d}/{:2d} Episodes'.format(  row['Title'],  row['Season'],  row['NbWatched'], row['NbDownloaded']))
        
    def getArguments(self, argv):
        parser = argparse.ArgumentParser(prog='missing_tvshows',  description='Parsing the local XBMC library for TV-Shows and discovers if new episodes are availalbe',  epilog='And that is how you use me')
        parser.add_argument("-i",  "--input",  help="input sqlite database file",  required=False,  metavar='DATABASE')
        parser.add_argument("-f",  "--force-update",  help="Force the update of the local TVDB Database",  required=False,  action="store_true",  dest='forceupdate')
        args = parser.parse_args(argv)
        self.__database = args.input or self.__database
        self.__forceUpdate = args.forceupdate
        self.checkXBMCDatabase()
        self.main()
        
        
if __name__ == "__main__":
    sms = TVShows()
    sms.getArguments(sys.argv[1:])
