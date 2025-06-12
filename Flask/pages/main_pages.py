from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User, Premium, Statics
from Flask.functions.functions import get_tasks, get_days
from Flask.database.constants import ICONS


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
                'task1_description': text1[2], 'task2_description': text2[2], 'task3_description': text3[2],

                'task1_icon': ICONS.get(text1[0], ICONS['other']),
                'task2_icon': ICONS.get(text2[0], ICONS['other']),
                'task3_icon': ICONS.get(text3[0], ICONS['other']),

                'task1_activity': text1[0].capitalize(),
                'task2_activity': text2[0].capitalize(),
                'task3_activity': text3[0].capitalize(),
            }

            return render_template('tasks.html', **data)
        else:
            return redirect('/login')

    @app.route("/statics")
    def statics():
        if current_user.is_authenticated:
            user = current_user
            name = user.name if len(user.name) < 10 else user.name[:7] + '...'

            statics = session.query(Statics).filter(Statics.user_id == user.id).first()
            total = statics.kilometres + statics.kilometre_swimming + statics.kilometre_bicycle
            total = 1 if total == 0 else total
            total_act = statics.push_up + statics.pull_up + statics.press + statics.squats
            total_act = 1 if total_act == 0 else total_act

            data = {
                'name': name, 'letter': name[0].upper(),

                'kilometres': statics.kilometres,
                'kilometres_stat': round((statics.kilometres / total) * 100),

                'bicycle': user.bike,
                'kilometre_bicycle': statics.kilometre_bicycle,
                'bicycle_stat': round((statics.kilometre_bicycle / total) * 100),

                'swimming': user.swimming,
                'kilometre_swimming': statics.kilometre_swimming,
                'swimming_stat': round((statics.kilometre_swimming / total) * 100),

                'pull_up': statics.pull_up, 'pull_up_stat': round((statics.pull_up / total_act) * 100),
                'push_up': statics.push_up, 'push_up_stat': round((statics.push_up / total_act) * 100),
                'press': statics.press, 'press_stat': round((statics.press / total_act) * 100),
                'squats': statics.squats, 'squats_stat': round((statics.squats / total_act) * 100),
            }

            return render_template('statics.html', **data)
        else:
            return redirect('/login')

    @app.route('/main', methods=['GET', 'POST'])
    def main_pa():
        if current_user.is_authenticated:
            user = current_user
            name = user.name if len(user.name) < 10 else user.name[:7] + '...'
            if request.method == 'POST':
                kilometre = request.form['kilometre']
                bicycle = request.form['bicycle']
                swim = request.form['swim']
                push_up = request.form['push_up']
                squats = request.form['squats']
                press = request.form['press']
                pull_up = request.form['pull_up']

                statics = session.query(Statics).filter(Statics.user_id == user.id).first()
                if kilometre not in [0.0, 0, '']:
                    statics.kilometres += float(kilometre)
                    statics.kilometres = 0.0 if statics.kilometres < 0.0 else statics.kilometres
                if bicycle not in [0.0, 0, '']:
                    statics.kilometre_bicycle += float(bicycle)
                    statics.kilometre_bicycle = 0.0 if statics.kilometre_bicycle < 0.0 else statics.kilometre_bicycle
                if swim not in [0.0, 0, '']:
                    statics.kilometre_swimming += float(swim)
                    statics.kilometre_swimming = 0.0 if statics.kilometre_swimming < 0.0 else statics.kilometre_swimming

                if push_up not in [0, '']:
                    statics.push_up += int(push_up)
                    statics.push_up = 0 if statics.push_up < 0 else statics.push_up
                if pull_up not in [0, '']:
                    statics.pull_up += int(pull_up)
                    statics.pull_up = 0 if statics.pull_up < 0 else statics.pull_up
                if squats not in [0, '']:
                    statics.squats += int(squats)
                    statics.squats = 0 if statics.squats < 0 else statics.squats
                if press not in [0, '']:
                    statics.press += int(press)
                    statics.press = 0 if statics.press < 0 else statics.press

                return render_template('main.html', name=name, letter=name[0].upper())
            else:
                return render_template('main.html', name=name, letter=name[0].upper())
        else:
            return redirect('/login')