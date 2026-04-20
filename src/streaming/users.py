"""
users.py
--------
Implement the class hierarchy for platform users.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sessions import ListeningSession


class User:
    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: list[ListeningSession] = []

    def add_session(self, session: "ListeningSession") -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(session.duration_listened_seconds for session in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        return {session.track.track_id for session in self.sessions}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.user_id!r})"


class FreeUser(User):
    MAX_SKIPS_PER_HOUR: int = 6

    def __init__(self, user_id: str, name: str, age: int) -> None:
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start: date | None = None,
    ) -> None:
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start: date | None = None,
    ) -> None:
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users: list[FamilyMember] = []

    def add_sub_user(self, sub_user: "FamilyMember") -> None:
        self.sub_users.append(sub_user)

    def all_members(self) -> list[User]:
        return [self, *self.sub_users]


class FamilyMember(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        parent: FamilyAccountUser,
    ) -> None:
        super().__init__(user_id, name, age)
        self.parent = parent