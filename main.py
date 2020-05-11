from flask import Flask, render_template, redirect
from flask_login import login_required, logout_user, current_user

from data import db_session
from data.users import User
from data.classs import Class
from data.subject import Subject
from data.lessons import Lessons

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

import flask_login


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = flask_login.login_manager.LoginManager()  # инициализация LoginManager
login_manager.init_app(app)


@login_manager.user_loader  # функция для получения пользователя
def load_user(user_id):
    session = db_session.create_session()  # создание сессии
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/School.sqlite")  # подключение к базе данных
    app.run()


class RegisterForm(FlaskForm):  # форма регистрации пользователя
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    klas = IntegerField('Класс', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):  # форма авторизации пользователя
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/')  # главная страница
def index():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])  # регистрация пользователя
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():  # проверяем зарегестрированную почту на уникальность
            # если на данную почту зарегистрирован другой пользователь, выводим сообщение
            return render_template('forma_register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        # создаем объект класса пользователя
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data,
            klas=form.klas.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')  # если регистрация успешна, переходим на страницу входа
    return render_template('forma_register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])  # вход в аккаунт
def login():
    form = LoginForm()
    if form.validate_on_submit():  #
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):  # проверка на правильность пароля
            flask_login.login_user(user)
            return redirect("/personal_account")  # если пароль и логин правильные, переходим в личный кабинет
        return render_template('forma_in.html',
                               message="Неправильный логин или пароль",
                               form=form)  # если неправильные, выводим сообщение
    return render_template('forma_in.html', title='Авторизация', form=form)


@app.route('/logout')  # выход из аккаунта
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/personal_account')  # личный кабинет пользователя
@login_required
def account():
    return render_template('personal_accaunt.html', name=current_user.name + ' ' + current_user.surname + '\t' + current_user.email)


@app.route('/get_class')  # страница выбора класса
@login_required
def get_class():
    session = db_session.create_session()
    b = session.query(Class).all()  # запоминаем предметы выбранного класса
    return render_template('get_class.html', title='Выбор класса', items=b, x=20)


@app.route('/get_subject/<int:my_id>')  # страница выбора предмета
@login_required
def get_subject(my_id):
    session = db_session.create_session()
    b = session.query(Subject).filter(Subject.clas_id == my_id).all()  # запоминаем уроки выбранного предмета
    return render_template('get_subject.html', title='Выбор предмета', items=b)


@app.route('/get_lesson/<int:my_id>')  # страница выбора урока
@login_required
def get_lesson(my_id):
    session = db_session.create_session()
    b = session.query(Lessons).filter(Lessons.subject_id == my_id).all()  # находим нужный урок
    return render_template('get_lessons.html', title='Выбор урока', items=b)


@app.route('/lesson/<int:my_id>')  # страница урока
@login_required
def lesson(my_id):
    session = db_session.create_session()
    b = session.query(Lessons).filter(Lessons.id == my_id).all()  # запоминаем текст урока для вывода на эеран
    return render_template('see_lesson.html', title='Урок', items=b)


if __name__ == '__main__':
    main()