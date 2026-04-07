from datetime import datetime, timedelta
from .users import PremiumUser, FamilyMember
from .tracks import Song
from .playlists import CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.catalogue = {}
        self.users = {}
        self.artists = {}
        self.albums = {}
        self.playlists = {}
        self.sessions = []

    def add_track(self, track):
        self.catalogue[track.track_id] = track

    def add_user(self, user):
        self.users[user.user_id] = user

    def add_artist(self, artist):
        self.artists[artist.artist_id] = artist

    def add_album(self, album):
        self.albums[album.album_id] = album

    def add_playlist(self, playlist):
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self.sessions.append(session)
        session.user.add_session(session)

    def all_users(self):
        return list(self.users.values())

    def all_tracks(self):
        return list(self.catalogue.values())

    def get_user(self, user_id):
        return self.users.get(user_id)

    # Q1
    def total_listening_time_minutes(self, start, end):
        total = 0.0
        for s in self.sessions:
            if start <= s.timestamp <= end:
                total += s.duration_listened_seconds / 60
        return total

    # Q2
    def avg_unique_tracks_per_premium_user(self, days=30):
        premium = []

        for u in self.users.values():
            if isinstance(u, PremiumUser):
                premium.append(u)

        if len(premium) == 0:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)

        counts = []
        for u in premium:
            tracks = set()
            for s in u.sessions:
                if s.timestamp >= cutoff:
                    tracks.add(s.track.track_id)
            counts.append(len(tracks))

        return sum(counts) / len(counts)

    # Q3
    def track_with_most_distinct_listeners(self):
        if len(self.sessions) == 0:
            return None

        data = {}

        for s in self.sessions:
            if s.track not in data:
                data[s.track] = set()
            data[s.track].add(s.user)

        best = None
        best_count = -1

        for t in data:
            if len(data[t]) > best_count:
                best = t
                best_count = len(data[t])

        return best

    # Q4
    def avg_session_duration_by_user_type(self):
        data = {}

        for s in self.sessions:
            t = type(s.user).__name__

            if t not in data:
                data[t] = []

            data[t].append(s.duration_listened_seconds)

        result = []

        for t in data:
            avg = sum(data[t]) / len(data[t])
            result.append((t, avg))

        result.sort(key=lambda x: x[1], reverse=True)

        return result

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total = 0.0

        for s in self.sessions:
            if isinstance(s.user, FamilyMember):
                if s.user.age < age_threshold:
                    total += s.duration_listened_seconds / 60

        return total

    # Q6
    def top_artists_by_listening_time(self, n=5):
        data = {}

        for s in self.sessions:
            if isinstance(s.track, Song):
                artist = s.track.artist

                if artist not in data:
                    data[artist] = 0.0

                data[artist] += s.duration_listened_seconds / 60

        result = list(data.items())
        result.sort(key=lambda x: x[1], reverse=True)

        return result[:n]

    # Q7
    def user_top_genre(self, user_id):
        user = self.users.get(user_id)

        if user is None or len(user.sessions) == 0:
            return None

        data = {}
        total = 0.0

        for s in user.sessions:
            g = s.track.genre
            m = s.duration_listened_seconds / 60

            if g not in data:
                data[g] = 0.0

            data[g] += m
            total += m

        best = None
        best_time = -1

        for g in data:
            if data[g] > best_time:
                best = g
                best_time = data[g]

        percentage = (best_time / total) * 100

        return (best, percentage)

    # Q8
    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []

        for p in self.playlists.values():
            if isinstance(p, CollaborativePlaylist):

                artists = set()

                for t in p.tracks:
                    if isinstance(t, Song):
                        artists.add(t.artist)

                if len(artists) > threshold:
                    result.append(p)

        return result

    # Q9
    def avg_tracks_per_playlist_type(self):
        normal = []
        collab = []

        for p in self.playlists.values():
            if isinstance(p, CollaborativePlaylist):
                collab.append(len(p.tracks))
            else:
                normal.append(len(p.tracks))

        return {
            "Playlist": sum(normal)/len(normal) if normal else 0.0,
            "CollaborativePlaylist": sum(collab)/len(collab) if collab else 0.0
        }

    # Q10
    def users_who_completed_albums(self):
        result = []

        for u in self.users.values():
            listened = set()

            for s in u.sessions:
                listened.add(s.track.track_id)

            completed = []

            for album in self.albums.values():
                if len(album.tracks) == 0:
                    continue

                ok = True

                for t in album.tracks:
                    if t.track_id not in listened:
                        ok = False
                        break

                if ok:
                    completed.append(album.title)

            if len(completed) > 0:
                result.append((u, completed))

        return result