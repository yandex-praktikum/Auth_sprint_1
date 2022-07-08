from email.policy import default
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
    
    social_accounts = db.relationship("SocialAccount", backref=db.backref('users.users', lazy=True))

    def __repr__(self):
        return f"<User {self.login}>"

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None, email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first() 

    def reset_oauth_field(self, social_type):
        SocialAccount.query(user_id=self.id, social_type=social_type).delete()

    def reset_oauth_fields(self):
        SocialAccount.query(user_id=self.id).delete()
        

class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.users.id'), nullable=False)
    social_type = db.Column(db.Text, nullable=False)
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)
    access_token = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),
                    {"schema": "users"},
                    )
    
    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>' 



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
    auth_type = Column(String, nullable=True, default=None)
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
