from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User


def main_pages(app, session):
    @app.route("/profile")
    def profile():
        if current_user.is_authenticated:
            name = current_user.name
            return name
        else:
            return redirect('/login')