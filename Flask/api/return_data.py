from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User, Premium, Statics, Tasks
from Flask.functions.functions import get_tasks, get_days
from Flask.database.constants import PASSWORD


def return_data(app, session):
    @app.route(f'/{PASSWORD}/name/<flask_id>')
    def return_name(flask_id):
        res = session.query(User).filter(User.id == int(flask_id)).first()
        print(res.name)
        return [res.name]

    @app.route(f'/{PASSWORD}/email/<email>')
    def check_email(email):
        res = session.query(User).filter(User.email == email).first()
        return '1' if res else '0'

    @app.route(f'/{PASSWORD}/password/<email>/<password>')
    def check_password(email, password):
        user = session.query(User).filter(User.email == email).first()
        return str(user.id) if user.check_password(password) else '0'

    @app.route(f'/{PASSWORD}/tasks/<flask_id>')
    def return_task(flask_id):
        user = session.query(User).filter(User.id == int(flask_id)).first()
        tasks = get_tasks(user, session)

        data = {
            'task1': [tasks.text1, tasks.task1],
            'task2': [tasks.text2, tasks.task2],
            'task3': [tasks.text3, tasks.task3]
        }

        return data

    @app.route(f'/{PASSWORD}/statistic/<flask_id>')
    def return_statistic(flask_id):
        user = session.query(User).filter(User.id == int(flask_id)).first()
        statics = session.query(Statics).filter(Statics.user_id == user.id).first()

        data = [
            ['🏃 Бег и ходьба', f"{statics.kilometres} км"],
            ['🏊 Велосипед', f"{statics.kilometre_bicycle} км"],
            ['🚴 Плавание', f"{statics.kilometre_swimming} км"],

            ['🔥 Подтягиваний', f"{statics.pull_up} раз"],
            ['🔥 Отжиманий', f"{statics.push_up} раз"],
            ['🔥 Упражнений на пресс', f"{statics.press} раз"],
            ['🔥 Приседаний', f"{statics.squats} раз"]
        ]

        return data

