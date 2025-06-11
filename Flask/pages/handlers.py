from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, AnonymousUserMixin
from Flask.database.database import User, Premium


def handlers(app, session):
    @app.route('/update_setting', methods=['POST'])
    def update_setting():
        data = request.get_json()
        setting_name = data.get('setting')
        user = current_user

        if data['setting'] == 'include_bicycle':
            user.bike = data['value']
        elif data['setting'] == 'include_swim':
            user.swimming = data['value']
        session.commit()

        print(f"Получено: {setting_name} = {data['value']}")

        return jsonify({"status": "success", "received": data})

    @app.route('/complete_task', methods=['POST'])
    def complete_task():
        data = request.get_json()
        task_id = data.get('task_id')

        print(f'Задача {task_id} выполнена пользователем.')

        return jsonify({
            'status': 'success',
            'message': f'Задача {task_id} отмечена как выполненная'
        })