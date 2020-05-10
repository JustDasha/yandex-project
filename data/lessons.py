import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Lessons(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    done = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("subject.id"))
    sub = orm.relation('Subject')
    users = orm.relation("User",
                 secondary="association",
                 backref="lessons", lazy='dynamic')
