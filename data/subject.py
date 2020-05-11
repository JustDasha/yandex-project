import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subject'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_of_subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя предмета
    clas_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("class.id"))  # поле связи с таблицей классов
    less = orm.relation("Lessons", back_populates='sub')  # связь с таблицей уроков
    clas = orm.relation("Class")  # связь с таблицей классов