from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from Flask.database.database import User, Statics



def registr(app, session):
    def is_valid_number(num: str):
        if len(num) in [11, 12]:
            if num.startswith('+'):
                num = num[1:]
            if num.startswith('8'):
                num = '7' + num[1:]
            if len(num) == 11 and num.startswith('79') and num.isdigit():
                return num
        return False

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
            num = is_valid_number(email)
            if not num:
                errors.append('Введите корректный номер телефона!')
            if session.query(User).filter_by(number=num).first():
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
                user = User(name=name, number=num)
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
            num = is_valid_number(email)
            if not num:
                errors.append('Введите корректный номер телефона!')
            if not session.query(User).filter_by(number=num).first():
                errors.append('Пользователя с этим номером телефона не зарегистрирован!')
            else:
                user = session.query(User).filter_by(number=num).first()
                if not user.check_password(password):
                    errors.append('Неверный пароль!')

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('login.html', email=num, message=errors[0])

            login_user(user, remember=True)
            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect("/index")