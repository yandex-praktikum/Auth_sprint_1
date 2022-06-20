import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin

from db.db import db


class User(db.Model, UserMixin):
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
