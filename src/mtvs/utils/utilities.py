import sys
import csv
import logging
from colorama import Fore, Style

__log = logging.getLogger("Tube4Droid")


def save_CSV(
    unwatched_finished_shows,
    unwatched_unfinished_shows,
    watchedsome_unfinished_shows,
    watchedsome_finished_shows,
):
    _write_CSV(watchedsome_finished_shows, "watchedsome_finished_shows.csv")
    _write_CSV(unwatched_unfinished_shows, "unwatched_unfinished_shows.csv")
    _write_CSV(watchedsome_unfinished_shows, "watchedsome_unfinished_shows.csv")


def _write_CSV(series, filename):
    __log.debug("Writing to " + filename)
    if sys.version_info >= (3, 0, 0):
        f = open(filename, "w", newline="")
    else:
        f = open(filename, "wb")
    with f:
        writer = csv.writer(f)
        writer.writerow(
            ["SeasonId", "Title", "Season", "Downloaded", "Available", "Missing"]
        )

        for show in series:
            writer.writerow(
                [
                    show["SeasonId"],
                    show["Title"].encode("utf-8"),
                    show["Season"],
                    show["NbDownloaded"],
                    show["NbAvailable"],
                    show["MissingEpisodes"],
                ]
            )
        f.close()


def print_konsole(
    unwatched_finished_shows,
    unwatched_unfinished_shows,
    watchedsome_unfinished_shows,
    watchedsome_finished_shows,
):
    sys.stdout.write('\n')
    print(Fore.RED + '##############################################################')
    print('###################### Unwatched Missing #####################')
    print('##############################################################' + Style.RESET_ALL)

    print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)
    print(Style.DIM + Fore.GREEN + '|' + Style.RESET_ALL + '{:44s} | {:s} ({:s}/{:s})| {:65s}|'.format('Title', 'Season', 'Downloaded', 'Available', 'Missing'))
    print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)
    for row in unwatched_unfinished_shows:
        print(Style.DIM + Fore.GREEN + '|' + Style.RESET_ALL + '{:43s}: | S{:2s} ({:2.0f}/{:2d})| missing: {:74s}|'.format(row['Title'], row['Season'], row['NbDownloaded'], row['NbAvailable'], row['MissingEpisodes']))
        print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)

    print(Fore.RED + '###############################################################')
    print('######################## Watched Missing ######################')
    print('###############################################################' + Style.RESET_ALL)
    print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)
    print(Style.DIM + Fore.GREEN + '|' + Style.RESET_ALL + '{:35s}({:8s})  | {:s} ({:s}/{:s})| {:65s}|'.format('Title', 'SeasonId', 'Season', 'Downloaded', 'Available', 'Missing'))
    print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)
    for row in watchedsome_unfinished_shows:
        print(Style.DIM + Fore.GREEN + '|' + Style.RESET_ALL + '{:35s}({:8s}): | S{:2s} ({:2.0f}/{:2d})| missing: {:74s}|'.format(row['Title'], row['SeasonId'], row['Season'], row['NbDownloaded'], row['NbAvailable'], row['MissingEpisodes']))
        print(Style.DIM + Fore.GREEN + '-------------------------------------------------------------------------------------------------------------------------------------------------' + Style.RESET_ALL)

    print(Fore.RED + '###############################################################')
    print('######################## Ready to Watch #######################')
    print('###############################################################' + Style.RESET_ALL)
    for row in unwatched_finished_shows:
        print('{:35s}: Season {:2s} and has {:2.0f}/{:2d} Episodes'.format(row['Title'], row['Season'], row['NbDownloaded'], row['NbAvailable']))

    print(Fore.RED + '###############################################################')
    print('#################### Complete and Watching ####################')
    print('###############################################################' + Style.RESET_ALL)
    for row in watchedsome_finished_shows:
        print('{:35s}: Season {:2s} and has watched {:2.0f}/{:2d} Episodes'.format(row['Title'], row['Season'], row['NbWatched'], row['NbDownloaded']))
