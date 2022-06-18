import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.db import db


class User(db.Model):
    __tablename__ = 'auth.users'

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
    password = Column(String,
                      nullable=False)
    role = Column(String,
                  default='registered',
                  nullable=False)


    def __repr__(self):
        return f'<User {self.login}>'
