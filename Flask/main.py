from flask import Flask
from flask_login import LoginManager

from Flask.database.database import Session, User

from Flask.pages.registr import registr
from Flask.pages.main_pages import main_pages
from Flask.pages.stated_pages import stated_pages
from Flask.pages.premium import premium
from Flask.pages.handlers import handlers
from Flask.api.return_data import return_data

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
    stated_pages(app, session)
    registr(app, session)
    premium(app, session)
    handlers(app, session)
    return_data(app, session)

    app.run(debug=True)
