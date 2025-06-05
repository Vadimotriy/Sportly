from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User


def main_pages(app, session):
    @app.route("/index")
    def index():
        if current_user.is_authenticated:
            return current_user.name
        else:
            return 'You are not logged in'