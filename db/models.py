import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, declarative_mixin, declared_attr

from db import Base
from db.engine import get_async_session


@declarative_mixin
class TimestampMixin:
    """Mixin with timestamp fields"""
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=datetime.datetime.now
    )


class User(TimestampMixin, SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'user'

    username = Column(String(30), index=True, unique=True, nullable=False)

    first_name = Column(String(30), nullable=False)
    second_name = Column(String(30), nullable=False)


@declarative_mixin
class CodeFileClass:
    @declared_attr
    def code_file(cls):
        return relationship('CodeFile')

    @declared_attr
    def code_file_id(cls):
        return Column(Integer, ForeignKey('code_files.id'), nullable=True)


class CodeCharacter(Base, CodeFileClass):
    __tablename__ = 'code_characters'

    first_name = Column(String(32), nullable=False)
    second_name = Column(String(32), nullable=False)

    description = Column(String(1024))


class CodeFraction(Base, CodeFileClass):
    __tablename__ = 'code_fractions'

    name = Column(String(64), nullable=False)

    description = Column(String(1024))


class CodeLocation(Base, CodeFileClass):
    __tablename__ = 'code_locations'

    name = Column(String(64), nullable=False)

    description = Column(String(1024))


class CodeItem(Base, CodeFileClass):
    __tablename__ = 'code_items'

    name = Column(String(64), nullable=False)

    description = Column(String(1024))


class CodeDifferent(Base, CodeFileClass):
    __tablename__ = 'code_difference'

    name = Column(String(64), nullable=False)

    description = Column(String(1024))


class CodeFile(Base):
    __tablename__ = 'code_files'

    file_format = Column(String(10), nullable=False)
    file_path = Column(String(1024), nullable=False)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
