"""
test_public.py
--------------
Public test suite template.

This file provides a minimal framework and examples to guide you in writing
comprehensive tests for your StreamingPlatform implementation. Each test class
corresponds to one of the 10 query methods (Q1-Q10).

You should:
1. Study the examples provided
2. Complete the stub tests (marked with TODO or pass statements)
3. Add additional test cases for edge cases and boundary conditions
4. Verify your implementation passes all tests

Run with:
    pytest tests/test_public.py -v
"""

from datetime import timedelta


# ================= Q1 =================
def test_total_listening_time(platform, recent_ts, fixed_now):
    result = platform.total_listening_time_minutes(recent_ts, fixed_now)

    # 120 + 180 + 200 = 500 sec → 500/60
    assert round(result, 2) == round(500 / 60, 2)


# ================= Q2 =================
def test_avg_unique_tracks(platform):
    result = platform.avg_unique_tracks_per_premium_user()

    # Bob listened to 2 unique tracks
    assert result == 2.0


# ================= Q3 =================
def test_track_most_listeners(platform):
    track = platform.track_with_most_distinct_listeners()

    assert track.track_id == "t1"


# ================= Q4 =================
def test_avg_session_duration(platform):
    result = platform.avg_session_duration_by_user_type()

    assert isinstance(result, list)
    assert len(result) > 0


# ================= Q5 =================
def test_underage_sub_users(platform):
    result = platform.total_listening_time_underage_sub_users_minutes()

    assert result == 0.0


# ================= Q6 =================
def test_top_artists(platform):
    result = platform.top_artists_by_listening_time()

    assert len(result) > 0
    assert result[0][1] > 0


# ================= Q7 =================
def test_user_top_genre(platform):
    result = platform.user_top_genre("u2")

    assert result is not None
    assert result[0] == "pop"


# ================= Q8 =================
def test_collaborative_playlists(platform):
    result = platform.collaborative_playlists_with_many_artists()

    assert isinstance(result, list)


# ================= Q9 =================
def test_avg_tracks_playlist(platform):
    result = platform.avg_tracks_per_playlist_type()

    assert "Playlist" in result
    assert "CollaborativePlaylist" in result


# ================= Q10 =================
def test_users_completed_albums(platform):
    result = platform.users_who_completed_albums()

    assert isinstance(result, list)