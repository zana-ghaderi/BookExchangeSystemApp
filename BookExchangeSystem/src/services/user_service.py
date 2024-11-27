import psycopg2
from Intuit.BookExchangeSystem.src.config.config import DB_CONFIG
import Intuit.BookExchangeSystem.src.database.database as db_util
from Intuit.BookExchangeSystem.src.models.user import User

class UserService:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.sessions = {}

    def user_exists(self, email):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            return cur.fetchone() is not None

    def get_user_by_email(self, email):
        with self.connection.cursor() as cur:
            cur.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            if user_data:
                return User(*user_data)
            return None
    def register_user(self, user):
        if self.user_exists(user.email):
            raise ValueError(f"User with email {user.email} already exists")

        columns = ['name', 'email', 'password_hash']
        values = [user.name, user.email, user.password_hash]
        user.user_id = db_util.insert_record('users', columns, values, self.connection)
        return user

    def get_user_by_id(self, user_id):
        columns = ['id', 'name', 'email', 'password_hash']
        user_data = db_util.get_record_by_id('users', columns, user_id, self.connection)
        if user_data:
            return User(*user_data)
        return None

    def update_user(self, user):
        columns = ['name', 'email', 'password_hash']
        values = [user.name, user.email, user.password_hash]
        db_util.update_record('users', columns, values, user.user_id, self.connection)
        return user

    def delete_user(self, user_id):
        db_util.delete_record('users', user_id, self.connection)

    def get_user_books(self, user_id):
        user = self.get_user_by_id(user_id)
        return user.owned_books if user else []

    def login(self, email, password):
        for user in self.get_all_users():
            if user.email == email and self.verify_password(password, user.password_hash):
                session_id = str(uuid.uuid4())
                self.sessions[session_id] = user
                return session_id
        raise ValueError("Invalid credentials")

    def logout(self, session_id):
        self.sessions.pop(session_id, None)

    def get_user_by_session(self, session_id):
        return self.sessions.get(session_id)

    def verify_password(self, password, password_hash):
        return hash(password) == password_hash

    def get_all_users(self):
        columns = ['id', 'name', 'email', 'password_hash']
        users_data = db_util.get_records('users', columns, self.connection)
        return [User(*user_data) for user_data in users_data]




import uuid


# class UserService:
#     def __init__(self):
#         self.users = {}
#         self.sessions = {}
#
#     def register_user(self, user):
#         self.users[user.user_id] = user
#         return user
#
#     def get_user_by_id(self, user_id):
#         return self.users.get(user_id)
#
#     def update_user(self, user):
#         if user.id not in self.users:
#             raise ValueError("User not found")
#         self.users[user.id] = user
#         return user
#
#     def delete_user(self, user_id):
#         self.users.pop(user_id, None)
#
#     def get_user_books(self, user_id):
#         user = self.get_user_by_id(user_id)
#         return user.owned_books if user else []
#
#     def login(self, email, password):
#         for user in self.users.values():
#             if user.email == email and self.verify_password(password, user.password_hash):
#                 session_id = str(uuid.uuid4())
#                 self.sessions[session_id] = user
#                 return session_id
#         raise ValueError("Invalid credentials")
#
#     def logout(self, session_id):
#         self.sessions.pop(session_id, None)
#         # logout all sessions
#         # self.active_sessions = {sid: user for sid, user in self.sessions.items() if user.id != user_id}
#
#     def get_user_by_session(self, session_id):
#         return self.sessions.get(session_id)
#
#     # this should be in password service
#     def verify_password(self, password, password_hash):
#         return hash(password) == password_hash
#
