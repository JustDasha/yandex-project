import sqlalchemy
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# ассоциативная таблица для связи пользователя и уроков(многое ко многим)
association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
    sqlalchemy.Column('users_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('lesson_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('lessons.id'))
)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # фамилия
    klas = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # класс
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)  # почта
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # пароль
    children = relationship("Lessons",
                            secondary=association_table)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
