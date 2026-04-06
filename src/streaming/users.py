"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def __repr__(self):
        return f"User({self.user_id})"


class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6


class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        return self.sub_users


class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent