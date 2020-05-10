from flask import Flask, render_template, redirect
from flask_login import login_required, logout_user

from data import db_session, forms
from data.users import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

import flask_login


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = flask_login.login_manager.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/School.sqlite")
    app.run()


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    klas = IntegerField('Класс', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('forma_register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
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
        return redirect('/login')
    return render_template('forma_register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        print(1)
        if user and user.check_password(form.password.data):
            flask_login.login_user(user)
            return redirect("/personal_account")
        return render_template('forma_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('forma_in.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/personal_account')
def account():
    return render_template('personal_accaunt.html')


@app.route('/vibor_lessons')
def vibor_lessons():
    return render_template('vibor_lessons.html')


if __name__ == '__main__':
    main()