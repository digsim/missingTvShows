import sys
from mtvs.main.mainImpl import MainImpl
from mtvs.Kodi.missing_tvshows import TVShows  # type: ignore


def main():
    """Entry point for the application script"""
    main = MainImpl()
    # sys.argv = ["missingTvShow", "sync"]
    main.getArguments(sys.argv[1:])
    tvs = TVShows("./tvdbdb.db", "api-key", "sqlite", "/test.db", "", "", "", "")
    tvs.__db


if __name__ == "__main__":
    main()
