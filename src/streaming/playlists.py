class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)
        self.contributors = []

    def add_contributor(self, user):
        self.contributors.append(user)