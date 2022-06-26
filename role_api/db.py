import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role = Column(String, unique=True, nullable=False, unique=True)
    description = Column(String, nullable=True)
    rule = Column(String, nullable=False)

    def __init__(self, role, description, rule):
        self.role = role
        self.description = description
        self.rule = rule

    def __repr__(self):
        return f'<Role {self.role}>'

class UserRole(Base):

    __tablename__ = 'user_role'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)