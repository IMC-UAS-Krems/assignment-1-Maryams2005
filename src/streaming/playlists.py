"""
playlists.py
------------
Represents user-created playlists.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track, Song
    from .users import User


class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: "User") -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list[Track] = []

    def add_track(self, track: "Track") -> None:
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        self.tracks = [t for t in self.tracks if t.track_id != track_id]

    def total_duration_seconds(self) -> int:
        return sum(t.duration_seconds for t in self.tracks)

    def track_count(self) -> int:
        return len(self.tracks)

    def __repr__(self) -> str:
        return f"Playlist({self.playlist_id!r}, {self.name!r})"


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner: "User") -> None:
        super().__init__(playlist_id, name, owner)
        self.contributors: list[User] = [owner]

    def add_contributor(self, user: "User") -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user: "User") -> None:
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)

    def all_contributors(self) -> list["User"]:
        return self.contributors

    def distinct_song_artists(self) -> set:
        artists = set()
        for track in self.tracks:
            if isinstance(track, Song):
                artists.add(track.artist)
        return artists