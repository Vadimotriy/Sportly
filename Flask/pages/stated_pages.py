from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User


def stated_pages(app, session):
    @app.route("/")
    @app.route("/index")
    def index():
        if current_user.is_authenticated:
            name = current_user.name
            name = name if len(name) < 10 else name[:7] + '...'
            return render_template('index_not_logged.html', text=current_user.name)
        else:
            return render_template('index_not_logged.html', text="Войти", logged=0)

    @app.route("/main")
    def main():
        if current_user.is_authenticated:
            name = current_user.name
            return name
        else:
            return redirect('/login')

    @app.route("/premium")
    def premium():
        if current_user.is_authenticated:
            user = current_user
            user.premium = 1
            session.commit()

            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'
            return render_template('premium.html', text=name)
        else:
            return redirect('/login')