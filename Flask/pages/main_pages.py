from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User, Premium
from Flask.functions.functions import get_tasks, get_days


def main_pages(app, session):
    @app.route("/profile")
    def profile():
        if current_user.is_authenticated:
            user = current_user

            name = user.name if len(user.name) < 10 else user.name[:7] + '...'
            fullname = user.name if len(user.name) < 30 else user.name[:28] + '...'
            meals = session.query(Premium).filter(Premium.user_id == user.id).all()

            percent_total = round((user.tasks_amount / ((get_days(user) + 1) * 3)) * 100)
            tasks_today = get_tasks(user, session)
            num = 1 if tasks_today.task1 is True else 0
            num += 1 if tasks_today.task2 is True else 0
            num += 1 if tasks_today.task3 is True else 0
            percent_today = round((num / 3) * 100)


            data = {
                'name': name,
                'fullname': fullname,
                'letter': name[0].upper(),
                'date_registr': user.created_date.strftime('%d.%m.%Y'),
                'dietolog_count': len(meals),
                'percent': f'{percent_total}%',
                'percent_today': f'{percent_today}%',
                'include_bicycle': user.bike,
                'include_swim': user.swimming
            }

            if meals:
                data['meals'] = meals[-1].text
                data['date'] = meals[-1].date.strftime('%d.%m.%Y')
                data['meal'] = 1
            else:
                data['meal'] = 0

            return render_template('profile.html', **data,)
        else:
            return redirect('/login')

    @app.route("/tasks")
    def tasks():
        if current_user.is_authenticated:
            user = current_user
            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'
            tasks = get_tasks(user, session)
            text1, text2, text3 = tasks.text1.split('__'), tasks.text2.split('__'), tasks.text3.split('__')

            data = {
                'name': name,
                'letter': name[0].upper(),

                'task1_status': tasks.task1, 'task2_status': tasks.task2, 'task3_status': tasks.task3,

                'task1_activity': text1[0].capitalize(),
                'task2_activity': text2[0].capitalize(),
                'task3_activity': text3[0].capitalize(),

                'task1_description': text1[2] + f' <b>{text1[1]}</b>',
                'task2_description': text2[2] + f' <b>{text2[1]}</b>',
                'task3_description': text3[2] + f' <b>{text3[1]}</b>',
            }

            return render_template('tasks.html', **data,)
        else:
            return redirect('/login')

