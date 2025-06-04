import re

from flask import Flask, render_template, request, redirect, url_for, flash

from Flask.database import db_session
from Flask.database.tables.users import User


def registr(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form_errors = []
        field_errors = {}
        name = email = ""

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            password_again = request.form.get('password_again')

            errors = []

            if not name:
                field_errors['name'] = 'Пожалуйста, введите ваше имя'

            if not email:
                field_errors['email'] = 'Пожалуйста, введите ваш email'
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                field_errors['email'] = 'Пожалуйста, введите корректный email'

            if not password:
                field_errors['password'] = 'Пожалуйста, введите пароль'
            elif len(password) < 8:
                field_errors['password'] = 'Пароль должен содержать не менее 8 символов'

            if not password_again:
                field_errors['password_again'] = 'Пожалуйста, повторите пароль'
            elif password != password_again:
                field_errors['password_again'] = 'Пароли не совпадают'

            # Проверка уникальности email
            if email and not field_errors.get('email'):
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    field_errors['email'] = 'Этот email уже зарегистрирован'

            db = db_session.create_session()
            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                field_errors['email'] = 'Пользователь с таким email уже зарегистрирован'

            # Если есть ошибки, показываем форму снова
            if field_errors:
                return render_template('register.html',
                                       errors=field_errors,
                                       form_errors=form_errors,
                                       name=name,
                                       email=email)

            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('register.html')

            try:
                new_user = User()
                new_user.set_password(password)

                user = User(name=name, email=email)
                user.set_password(password)
                db.add(user)
                db.commit()

                flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
                return redirect(url_for('login'))

            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при регистрации: {str(e)}', 'danger')
                app.logger.error(f'Registration error: {str(e)}')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return ''