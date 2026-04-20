"""
platform.py
-----------
Central orchestration layer for the music streaming platform.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from .albums import Album
from .artists import Artist
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession
from .tracks import Track, Song
from .users import User, PremiumUser, FamilyMember


class StreamingPlatform:
    def __init__(self, name: str) -> None:
        self.name = name
        self.catalogue: dict[str, Track] = {}
        self.users: dict[str, User] = {}
        self.artists: dict[str, Artist] = {}
        self.albums: dict[str, Album] = {}
        self.playlists: dict[str, Playlist] = {}
        self.sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self.catalogue[track.track_id] = track

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self.artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self.albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession) -> None:
        self.sessions.append(session)
        if session not in session.user.sessions:
            session.user.add_session(session)

    def get_track(self, track_id: str) -> Optional[Track]:
        return self.catalogue.get(track_id)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_artist(self, artist_id: str) -> Optional[Artist]:
        return self.artists.get(artist_id)

    def get_album(self, album_id: str) -> Optional[Album]:
        return self.albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self.users.values())

    def all_tracks(self) -> list[Track]:
        return list(self.catalogue.values())

    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total = 0.0
        for session in self.sessions:
            if start <= session.timestamp <= end:
                total += session.duration_listened_minutes()
        return total

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = [
            user for user in self.users.values()
            if isinstance(user, PremiumUser)
        ]

        if not premium_users:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)
        unique_track_counts: list[int] = []

        for user in premium_users:
            listened_track_ids = {
                session.track.track_id
                for session in user.sessions
                if session.timestamp >= cutoff
            }
            unique_track_counts.append(len(listened_track_ids))

        return sum(unique_track_counts) / len(unique_track_counts)

    def track_with_most_distinct_listeners(self) -> Optional[Track]:
        if not self.sessions:
            return None

        listeners_per_track: dict[Track, set[User]] = {}

        for session in self.sessions:
            if session.track not in listeners_per_track:
                listeners_per_track[session.track] = set()
            listeners_per_track[session.track].add(session.user)

        best_track = None
        best_count = -1

        for track, listeners in listeners_per_track.items():
            if len(listeners) > best_count:
                best_track = track
                best_count = len(listeners)

        return best_track

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        durations_by_type: dict[str, list[int]] = {}

        for session in self.sessions:
            type_name = type(session.user).__name__
            if type_name not in durations_by_type:
                durations_by_type[type_name] = []
            durations_by_type[type_name].append(session.duration_listened_seconds)

        result: list[tuple[str, float]] = []
        for type_name, durations in durations_by_type.items():
            result.append((type_name, sum(durations) / len(durations)))

        result.sort(key=lambda item: item[1], reverse=True)
        return result

    def total_listening_time_underage_sub_users_minutes(
        self,
        age_threshold: int = 18,
    ) -> float:
        total = 0.0

        for session in self.sessions:
            if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
                total += session.duration_listened_minutes()

        return total

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        listening_time_by_artist: dict[Artist, float] = {}

        for session in self.sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                if artist not in listening_time_by_artist:
                    listening_time_by_artist[artist] = 0.0
                listening_time_by_artist[artist] += session.duration_listened_minutes()

        result = list(listening_time_by_artist.items())
        result.sort(key=lambda item: item[1], reverse=True)
        return result[:n]

    def user_top_genre(self, user_id: str) -> Optional[tuple[str, float]]:
        user = self.users.get(user_id)
        if user is None or not user.sessions:
            return None

        minutes_by_genre: dict[str, float] = {}
        total_minutes = 0.0

        for session in user.sessions:
            genre = session.track.genre
            minutes = session.duration_listened_minutes()

            if genre not in minutes_by_genre:
                minutes_by_genre[genre] = 0.0

            minutes_by_genre[genre] += minutes
            total_minutes += minutes

        top_genre: str | None = None
        top_minutes = -1.0

        for genre, minutes in minutes_by_genre.items():
            if minutes > top_minutes:
                top_genre = genre
                top_minutes = minutes

        percentage = (top_minutes / total_minutes) * 100.0

        return (top_genre, percentage) if top_genre is not None else None

    def collaborative_playlists_with_many_artists(
        self,
        threshold: int = 3,
    ) -> list[CollaborativePlaylist]:
        result: list[CollaborativePlaylist] = []

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)

                if len(artists) > threshold:
                    result.append(playlist)

        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        normal_counts: list[int] = []
        collaborative_counts: list[int] = []

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative_counts.append(len(playlist.tracks))
            else:
                normal_counts.append(len(playlist.tracks))

        return {
            "Playlist": (
                sum(normal_counts) / len(normal_counts)
                if normal_counts else 0.0
            ),
            "CollaborativePlaylist": (
                sum(collaborative_counts) / len(collaborative_counts)
                if collaborative_counts else 0.0
            ),
        }

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result: list[tuple[User, list[str]]] = []

        for user in self.users.values():
            listened_track_ids = {session.track.track_id for session in user.sessions}
            completed_album_titles: list[str] = []

            for album in self.albums.values():
                if not album.tracks:
                    continue

                album_track_ids = {track.track_id for track in album.tracks}
                if album_track_ids.issubset(listened_track_ids):
                    completed_album_titles.append(album.title)

            if completed_album_titles:
                result.append((user, completed_album_titles))

        return result