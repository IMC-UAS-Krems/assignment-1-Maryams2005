"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.
"""

from __future__ import annotations

from abc import ABC


class Track(ABC):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
    ) -> None:
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0

    def __eq__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __hash__(self) -> int:
        return hash(self.track_id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.track_id!r}, {self.title!r})"


class Song(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist
        if artist is not None:
            artist.add_track(self)


class SingleRelease(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
        release_date,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class AlbumTrack(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist,
        track_number: int = 0,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.album = None
        self.track_number = track_number


class Podcast(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        description: str = "",
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class InterviewEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        guest: str,
        description: str = "",
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class NarrativeEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str,
        season: int,
        episode_number: int,
        description: str = "",
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number


class AudiobookTrack(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        author: str,
        narrator: str,
    ) -> None:
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator