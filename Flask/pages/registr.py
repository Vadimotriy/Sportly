import re

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.sql.functions import user

from Flask.database.database import User, Statics
from flask_login import login_user, logout_user, current_user


def registr(app, session):
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['password_again']

            errors = []

            if not name or len(name) < 3:
                errors.append('Имя должно содержать минимум 3 символа!')
            if not is_valid_email(email):
                errors.append('Введите корректный email!')
            if session.query(User).filter_by(email=email).first():
                errors.append('Этот email уже используется!')
            if len(password) < 8:
                errors.append('Пароль должен содержать минимум 8 символов!')
            if password != confirm_password:
                errors.append('Пароли не совпадают!')

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('register.html', name=name, email=email, message=errors[0])

            try:
                user = User(name=name, email=email)
                user.set_password(password)
                session.add(user)
                session.commit()

                statistic = Statics(user_id=user.id)
                session.add(statistic)
                session.commit()

                flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
                return redirect(url_for('login'))

            except Exception as e:
                print(e)

        return render_template('register.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            errors = []

            if not is_valid_email(email):
                errors.append('Введите корректный email!')
            if not session.query(User).filter_by(email=email).first():
                errors.append('Пользователя с этим email не зарегистрирован!')
            else:
                user = session.query(User).filter_by(email=email).first()
                if not user.check_password(password):
                    errors.append('Неверный пароль!')

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('login.html', email=email, message=errors[0])

            login_user(user, remember=True)
            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect("/index")