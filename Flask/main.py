from flask import Flask, render_template, request, redirect, url_for
from Flask.database.database import Session

from Flask.pages.main_pages import main_pages
from Flask.pages.registr import registr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
session = Session()


if __name__ == '__main__':
    main_pages(app, session)
    registr(app, session)
    app.run(debug=True)


