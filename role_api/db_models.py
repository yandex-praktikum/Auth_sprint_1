# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

import uuid
from flask import Flask
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db import db

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'roles'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    rule = Column(String, nullable=False)

    def __init__(self, role, description, rule):
        self.role = role
        self.description = description
        self.rule = rule

    def __repr__(self):
        return f'<Role {self.role}>'

class UserRole(db.Model):

    __tablename__ = 'user_role'
    __table_args__ = {'schema': 'roles'}

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
