import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subject'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    clas_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("class.id"))
    less = orm.relation("Lessons", back_populates='sub')
    clas = orm.relation("Class")