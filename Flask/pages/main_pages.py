from flask import Flask, render_template, request, redirect, url_for
from Flask.database.database import User


def main_pages(app, session):
    @app.route("/")
    def index():
        return redirect(url_for('register'))

        users = session.query(User)
        for user in users:
            print(user.statics)
        return render_template("index.html", news=users)