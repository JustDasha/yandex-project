import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subject'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    less = orm.relation("Lessons", back_populates='sub')