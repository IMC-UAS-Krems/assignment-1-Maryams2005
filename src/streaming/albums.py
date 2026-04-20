"""
albums.py
---------
Represents an ordered collection of AlbumTrack objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import AlbumTrack
    from .artists import Artist


class Album:
    """Ordered collection of AlbumTrack objects."""

    def __init__(
        self,
        album_id: str,
        title: str,
        artist: Artist,
        release_year: int,
    ) -> None:
        self.album_id: str = album_id
        self.title: str = title
        self.artist: Artist = artist
        self.release_year: int = release_year
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: "AlbumTrack") -> None:
        if track not in self.tracks:
            track.album = self
            self.tracks.append(track)
            self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self) -> set[str]:
        return {track.track_id for track in self.tracks}

    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)

    def total_duration_seconds(self) -> int:
        return self.duration_seconds()

    def total_duration_minutes(self) -> float:
        return self.duration_seconds() / 60.0

    def track_count(self) -> int:
        return len(self.tracks)

    def __repr__(self) -> str:
        return f"Album({self.album_id!r}, {self.title!r})"