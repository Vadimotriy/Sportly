from flask import Flask, render_template, request, redirect, url_for
from Flask.database import db_session

from Flask.pages.main_pages import main_pages

app = Flask(__name__, static_folder="data/static", template_folder="data/templates")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("Flask/data/test.db")


if __name__ == '__main__':
    main_pages(app)
    app.run(debug=True)


