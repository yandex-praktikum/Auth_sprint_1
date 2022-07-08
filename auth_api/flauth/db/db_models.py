from typing import Optional
import uuid
from datetime import datetime
import string
from secrets import choice as secrets_choice

from sqlalchemy import Column, DateTime, String, UniqueConstraint, or_
from sqlalchemy.dialects.postgresql import UUID

from db.db import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    role = Column(String, default="registered", nullable=False)
    google_id = Column(String, nullable=True)
    google_token = Column(String, nullable=True)
    yandex_id = Column(String, nullable=True)
    yandex_token = Column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.login}>"

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first() 

    def reset_oauth_fields(self):
        self.google_id = None
        self.google_token = None
        self.yandex_id = None
        self.yandex_token = None

class AuthRecord(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True), nullable=False)
    user_agent = Column(String, nullable=False)
    auth_type = Column(String, nullable=True)
    date_time = Column(DateTime, default=datetime.now(), nullable=False)


class RefreshToken(db.Model):
    __tablename__ = "refresh"
    __table_args__ = {"schema": "users"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True), nullable=False)
    user_agent = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)


def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16)) 
