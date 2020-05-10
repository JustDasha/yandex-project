from flask import Flask, render_template, redirect
from data import db_session, forms
from data.users import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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


@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(1)
    if form.validate_on_submit():
        session = db_session.create_session()
        print(2)
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('forma_register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        print(3)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data,
            klas=form.klas.data
        )
        print(4)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('forma_register.html', title='Регистрация', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('forma_in.html')


@app.route('/personal_account', methods=['GET', 'POST'])
def account():
    return render_template('personal_accaunt.html')


@app.route('/vibor_lessons', methods=['GET', 'POST'])
def vibor_lessons():
    return render_template('vibor_lessons.html')


if __name__ == '__main__':
    main()