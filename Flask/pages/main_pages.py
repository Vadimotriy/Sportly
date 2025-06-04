from flask import Flask, render_template, request, redirect, url_for

from Flask.database import db_session
from Flask.database.tables.users import User
from Flask.database.tables.statics import Statics


def main_pages(app):
    @app.route("/")
    def index():
        db_sess = db_session.create_session()
        users = db_sess.query(User)
        for user in users:
            print(user.statics)
        return render_template("index.html", news=users)