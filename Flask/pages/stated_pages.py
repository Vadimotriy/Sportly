from flask import render_template
from flask_login import current_user


def stated_pages(app, session):
    @app.route("/")
    @app.route("/index")
    def index():
        if current_user.is_authenticated:
            name = current_user.name
            name = name if len(name) < 10 else name[:7] + '...'
            return render_template('index_not_logged.html', text=name)
        else:
            return render_template('index_not_logged.html', text="Войти", logged=0)

    @app.route("/premium/info")
    def premium_info():
        if current_user.is_authenticated:
            user = current_user
            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'
            return render_template('premium-info.html', text=name)
        else:
            return render_template('premium-info.html', text='Войти')
