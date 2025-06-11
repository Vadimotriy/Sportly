from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User, Premium


def main_pages(app, session):
    @app.route("/profile")
    def profile():
        if current_user.is_authenticated:
            user = current_user

            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'
            fullname = name if len(name) < 30 else name[:28] + '...'

            meals = session.query(Premium).filter(Premium.user_id == user.id).all()
            print(meals)

            data = {
                'name': name,
                'fullname': fullname,
                'letter': name[0].upper(),
                'date_registr': user.created_date.strftime('%d.%m.%Y'),
                'dietolog_count': len(meals),
                'percent': '0%',
                'percent_today': '0%'
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