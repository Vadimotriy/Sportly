from flask import Flask, render_template, request, redirect, url_for
from Flask.database import db_session

from Flask.pages.main_pages import main_pages
from Flask.pages.registr import registr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("Flask/data/test.db")


if __name__ == '__main__':
    main_pages(app)
    registr(app)
    app.run(debug=True)


