from typing_extensions import TypedDict


class MtvsTvShow(TypedDict):
    Title: str
    SeasonId: int
    Season: int
    NbDownloaded: int
    NbAvailable: int
    NbWatched: int
    MissingEpisodes: str
