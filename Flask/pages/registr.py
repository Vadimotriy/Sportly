import re

from flask import Flask, render_template, request, redirect, url_for, flash
from Flask.database.database import User


def registr(app, session):
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        print(request.method)
        if request.method == 'POST':
            print(2)
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

            print(errors)
            print(3)

            if errors:
                for error in errors:
                    print(error)
                    flash(error, 'error')
                return render_template('register.html', name=name, email=email, message=errors[0])

            try:
                print(4)
                user = User(name=name, email=email)
                user.set_password(password)
                session.add(user)
                session.commit()
                print(5)

                flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
                return redirect(url_for('login'))

            except Exception as e:
                print(e)
        print(0)
        return render_template('register.html')


    @app.route('/login', methods=['GET'])
    def login():
        return "Страница входа (здесь будет форма входа)"