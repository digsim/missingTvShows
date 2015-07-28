# missing_tv_shows_for_xbmc


Missing TV-Shows for Kodi is a small python utility to check which episodes are still missing. Sometimes it is hard to keep up with multiple series and keep our collections clean and full. This small script iterates over all availalbe series in Kodi and checks whether they some episodes are missing.


## Introduction

To find missing episodes, for each season of each series, the script asks thetvdb.com for the total amount of episodes in this particular season. Based on the response from thetvdb and the information in the local Kodi databse, the scripts computes the missing episodes.

The output is either:
* command line only. The information is structured into four parts
* CSV files. The information is spread upon three files.

The command line output is structured into the following four sections:

1. All episods unwatched & Some episodes still missing
2. Some episodes alread watched & Some episodes still missing
3. All episodes unwatched & All episodes downloaded
4. Some episodes already watched & All episodes downloaded

Since TheTVDB gets constantly updated (for running seasons), it is possible that a given season is sometimes in section 2) and sometimes in section 4). However, if the season is locked on thetvdb, the information is accurate and once a a series arrives in section 4, it will stay there.

There is no section containing complete and watched episodes as I judge this infomration not relevant here. Thus, as soon as for a given season all episodes are collected and watched, it will dissapear from the list.


## Usage

A Sample output may be look like this:
```
:src$ missingTVShows
Acquiring necessary TV-Shows information
[===============================================================================================     ] 95%
##############################################################
###################### Unwatched Missing #####################
##############################################################
-------------------------------------------------------------------------------------------------------------------------------------------------
|Title                                        | Season (Downloaded/Available)| Missing                                                                   |
-------------------------------------------------------------------------------------------------------------------------------------------------
|Gold Rush                                    : | S3  ( 2/17)| missing: 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17                        |
-------------------------------------------------------------------------------------------------------------------------------------------------
###############################################################
######################## Watched Missing ######################
###############################################################
-------------------------------------------------------------------------------------------------------------------------------------------------
|Title                              (SeasonId)  | Season (Downloaded/Available)| Missing                                                                   |
-------------------------------------------------------------------------------------------------------------------------------------------------
|fernOST - Von Berlin nach Tokio    (275486  ): | S1  (10/11)| missing: 11                                                                        |
-------------------------------------------------------------------------------------------------------------------------------------------------
###############################################################
######################## Ready to Watch #######################
###############################################################
Big Rig Bounty Hunters             : Season 1  and has 8/8 Episodes
Doomsday Preppers                  : Season 2  and has 18/18 Episodes
Doomsday Preppers                  : Season 3  and has 14/14 Episodes
###############################################################
#################### Complete and Watching ####################
###############################################################
Doomsday Preppers                  : Season 1  and has watched  8/12 Episodes

```

# Installation

## From pip

Simply run
```
pip install missingTVShows
```

## From Sources

### Final installation

From a terminal launch
```
sudo python setup.py install --record files.txt
```
this will compile and install the project to the pyhton libraries (eg. /usr/local/lib/python2.7/dist-packages/XWoT_Model_Translator-1.1-py2.7.egg). Furthermore it will install a script in /usr/local/bin/:
* missingTVShows

The basic configuration and logging.conf are copied into /etc/MissingTVShows/. Upon the first start a copy of this directory is created in the user's home directory ~/.MissingTVShows/. From this point on configuration files are read from this location. It is however possible to overwrite them either by placing a file with the same name (but prefixed with a dot eg. .logging.conf) in the user home directory or a file with the same name in the current working directory.

### Development installation

from a terminal launch
```
sudo python setup.py develop --record files.txt
```
does the same as before but, uses links instead of copying files.

### Clean Working directory

To clean the working directory
```
sudo python setup.py clean --all
sudo rm -rf build/ dist/ Identify_missing_TVShows_in_Kodi.egg-info/ files.txt
```

# Uninstall

## Method 1
```
pip uninstall missingTVShows
```

## Method 2 (if installed from sources)
```
cat files.txt |sudo xargs rm -rf
```
## Method 3  (if installed from sources)

First find the installed package with pip and the uninstall it
```
✔ ~/Documents/Programming/Python/missing_tv_shows_for_xbmc [master ↑·1|✚ 1]
12:11 $ pip freeze |grep Identify-missing-TVShows
Identify-missing-TVShows-in-Kodi==1.1
✔ ~/Documents/Programming/Python/missing_tv_shows_for_xbmc [master ↑·1|✚ 1]
12:11 $ sudo pip uninstall Identify-missing-TVShows-in-Kodi
Password:
Uninstalling Identify-missing-TVShows-in-Kodi:
  /Library/Python/2.7/site-packages/Identify_missing_TVShows_in_Kodi-1.1-py2.7.egg
  /usr/local/bin/missingTVShows
Proceed (y/n)? y
  Successfully uninstalled Identify-missing-TVShows-in-Kodi
✔ ~/Documents/Programming/Python/missing_tv_shows_for_xbmc [master ↑·1|✚ 1]
12:12 $
```

# Configuration

Upon the first launch, the script creates the ~/.MissingTVShows/ directory containing:
* logging.conf where the logger is configured
* tvshows.cfg where the general configuration is stored. Adapt at least the <db> property and point it to the Kodi MyVideosXX.db. This file is usually found under
    * On Linux system this files is usually: /home/<username>/.kodi/userdata/Database/MyVideos93.db
    * On Mac OsX the file is found under: /Users/<username>/Library/Application Support/Kodi/userdata/Database/MyVideos93.db
    * Under Windows there must me a simliar location ;-)
* tvdbdb.db the local TheTVDB.com cache as SQLite file

