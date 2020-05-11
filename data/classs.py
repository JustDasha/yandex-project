import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase):
    __tablename__ = 'class'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя класса
    sub = orm.relation("Subject", back_populates='clas')  # связь с таблицей предметов