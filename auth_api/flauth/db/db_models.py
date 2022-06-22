import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
    login = Column(String,
                   unique=True,
                   nullable=False)
    name = Column(String,
                  nullable=True)
    email = Column(String,
                   unique=True,
                   nullable=False)
    hash_password = Column(String,
                           nullable=False)
    role = Column(String,
                  default='registered',
                  nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


class AuthRecord(db.Model):
    __tablename__ = 'auth'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)

    user_id = Column(UUID(as_uuid=True),
                     nullable=False)

    user_agent = Column(String,
                        nullable=False)

    data_time = Column(DateTime,
                       default=datetime.now(),
                       nullable=False)

