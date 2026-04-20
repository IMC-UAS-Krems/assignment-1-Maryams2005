"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import AlbumTrack
from streaming.users import FreeUser, PremiumUser
from streaming.sessions import ListeningSession


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # inside 30-day window
OLD = FIXED_NOW - timedelta(days=60)      # outside 30-day window


# ---------------------------------------------------------------------------
# Main platform fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def platform():
    platform = StreamingPlatform("TestStream")

    # ------------------ Artist ------------------
    artist = Artist("a1", "Pixels", "pop")
    platform.add_artist(artist)

    # ------------------ Album + Tracks ------------------
    album = Album("alb1", "Digital Dreams", artist, 2022)

    t1 = AlbumTrack("t1", "Track1", 180, "pop", artist, 1)
    t2 = AlbumTrack("t2", "Track2", 200, "pop", artist, 2)

    album.add_track(t1)
    album.add_track(t2)

    platform.add_album(album)
    platform.add_track(t1)
    platform.add_track(t2)

    # ------------------ Users ------------------
    u1 = FreeUser("u1", "Alice", 30)
    u2 = PremiumUser("u2", "Bob", 25, date(2023, 1, 1))

    platform.add_user(u1)
    platform.add_user(u2)

    # ------------------ Sessions ------------------
    s1 = ListeningSession("s1", u1, t1, RECENT, 120)
    s2 = ListeningSession("s2", u2, t1, RECENT, 180)
    s3 = ListeningSession("s3", u2, t2, RECENT, 200)

    platform.record_session(s1)
    platform.record_session(s2)
    platform.record_session(s3)

    return platform
# ---------------------------------------------------------------------------
# Time fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def fixed_now():
    return FIXED_NOW


@pytest.fixture
def recent_ts():
    return RECENT


@pytest.fixture
def old_ts():
    # timestamp outside 30-day window for testing filtering logic
    return OLD   