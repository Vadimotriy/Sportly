from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User


def premium(app, session):
    @app.route("/premium/get")
    def premium_get():
        if current_user.is_authenticated:
            user = current_user
            user.premium += 2
            session.commit()

            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'
            return render_template('premium.html', text=name)
        else:
            return redirect('/login')

