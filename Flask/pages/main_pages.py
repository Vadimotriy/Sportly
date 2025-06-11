from flask import Flask, render_template, request, redirect, url_for, jsonify
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

            data = {
                'name': name,
                'fullname': fullname,
                'letter': name[0].upper(),
                'date_registr': user.created_date.strftime('%d.%m.%Y'),
                'dietolog_count': len(meals),
                'percent': '0%',
                'percent_today': '0%',
                'include_bicycle': user.bike,
                'include_swim': user.swimming
            }
            print(user.bike, user.swimming)
            if meals:
                data['meals'] = meals[-1].text
                data['date'] = meals[-1].date.strftime('%d.%m.%Y')
                data['meal'] = 1
            else:
                data['meal'] = 0

            return render_template('profile.html', **data,)
        else:
            return redirect('/login')

    @app.route('/update_setting', methods=['POST'])
    def update_setting():
        data = request.get_json()
        setting_name = data.get('setting')
        user = current_user

        if data['setting'] == 'include_bicycle':
            user.bike = data['value']
        elif data['setting'] == 'include_swim':
            user.swimming = data['value']

        print(f"Получено: {setting_name} = {data['value']}")

        return jsonify({"status": "success", "received": data})