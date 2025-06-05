from flask import Flask, render_template, request, redirect, url_for
from Flask.database.database import Session
from Flask.database.database import User

from Flask.pages.main_pages import main_pages
from Flask.pages.registr import registr
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
session = Session()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


if __name__ == '__main__':
    main_pages(app, session)
    registr(app, session)
    app.run(debug=True)


