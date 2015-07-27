# missing_tv_shows_for_xbmc


Missing TV-Shows for XBMC is a small python utility to check which episodes are still missing. Sometimes it is hard to keep up with multiple series and keep our collections clean and full. This small script iterates over all availalbe series in XBMC and checks whether they some episodes are missing.


## Introduction

To find missing episodes, for each season of each series, the script asks thetvdb.com for the total amount of episodes in this particular season. Based on the response from thetvdb and the information in the local XBMC databse, the scripts computes the missing episodes.

The outpout is command line only. The information is structured into four parts

1. All episods unwatched & Some episodes still missing
2. Some episodes alread watched & Some episodes still missing
3. All episodes unwatched & All episodes downloaded
4. Some episodes already watched & All episodes downloaded

Depending on the frequency thetvdb is updated. It is very possible that a given season is sometimes in section 2) and sometimes in section 4). However, if the season is locked on thetvdb, the information is accurate and once a a series arrives in section 4, it will stay there.

There is no section containing complete and watched episodes as I judge this infomration not relevant here. Thus, as soon as for a given season all episodes are collected and watched, it will dissapear from the list.


## Usage

A Sample output may be look like this:
```
:src$ python missing_tvshows.py
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

## Configuration

To use the script, install the necessary reuquirements by exectuing:
```
sudo pip install -r requirements.txt
```
alternatively install the requirements by hand (into a virtual environment).

The script relys on a configuration file, tvshows.cfg. It only contains a few switches for thetvdb API keys and where to store locally cached information. However, there is one option which needs to be adapted to follow the configuration of your system. This is the *db* property pointing to the XBMC sqlite file for the movie information (called *MyVideos93.db*). In order to have the script running successfully this property needs to be set,
* On Linux system this files is usually: /home/<username>/.kodi/userdata/Database/MyVideos90.db
* On Mac OsX the file is found under: /Users/<username>/Library/Application Support/Kodi/userdata/Database/MyVideos90.db
* Under Windows there must me a simliar location ;-)
