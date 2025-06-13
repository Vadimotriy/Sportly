from flask import render_template, request, redirect
from flask_login import current_user

from Flask.database.database import Premium
from Flask.functions.dietolog import analyze


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

    @app.route("/premium/dietolog", methods=['GET', 'POST'])
    def premium_dietolog():
        if current_user.is_authenticated:
            user = current_user
            attempts = user.premium
            if attempts <= 0:
                return redirect('/premium/info')

            name = user.name
            name = name if len(name) < 10 else name[:7] + '...'

            if request.method == 'GET':
                return render_template('premium-dietolog.html', name=name, letter=name[0].upper(),
                                       attempts_left=attempts)
            elif request.method == 'POST':
                age = request.form['age']
                weight = request.form['weight']
                height = request.form['height']
                preferences = request.form['preferences']
                dislikes = request.form['dislikes']
                purpose = request.form['purpose']
                life = request.form['life']
                cant = request.form['cant']

                result = analyze(age, weight, height, preferences, dislikes, purpose, life, cant)

                user.premium -= 1
                attempts = user.premium
                premium = Premium(user_id=user.id, text=result)
                session.add(premium)
                session.commit()

                return render_template('dietolog-res.html', text=result, name=name,
                                       letter=name[0].upper(), attempts_left=attempts)
            return redirect('/premium')

        else:
            return redirect('/login')
