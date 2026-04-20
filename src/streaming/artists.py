"""
artists.py
----------
Represents music artists and their associated tracks.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track


class Artist:
    """Music artist or content creator."""

    def __init__(self, artist_id: str, name: str, genre: str) -> None:
        self.artist_id: str = artist_id
        self.name: str = name
        self.genre: str = genre
        self.tracks: list[Track] = []

    def add_track(self, track: "Track") -> None:
        """Add a track to this artist if not already present."""
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self) -> int:
        """Return the number of tracks associated with this artist."""
        return len(self.tracks)

    def __repr__(self) -> str:
        return f"Artist({self.artist_id!r}, {self.name!r})"