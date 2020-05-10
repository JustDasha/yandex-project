from flask import Flask, render_template
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/School.sqlite")
    app.run()


@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('forma_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('forma_in.html')


if __name__ == '__main__':
    main()