import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Lessons(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя урока
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # наполнение урока
    subject_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("subject.id"))  # связь с таблицей предметов
    sub = orm.relation('Subject')
    users = orm.relation("User",
                 secondary="association",
                 backref="lessons", lazy='dynamic')  # связь с таблицей пользователя
