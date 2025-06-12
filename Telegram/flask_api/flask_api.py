import requests

from Telegram.database.constants import PASSWORD


def get_name(flask_id):
    response = requests.get(f'http://127.0.0.1:5000/{PASSWORD}/name/{flask_id}')
    return response.json()[0]

def checkemail(email):
    response = requests.get(f'http://127.0.0.1:5000/{PASSWORD}/email/{email}')
    return response.json()

def check_password(email, password):
    response = requests.get(f'http://127.0.0.1:5000/{PASSWORD}/password/{email}/{password}')
    return response.json()

def get_tasks(flask_id):
    response = requests.get(f'http://127.0.0.1:5000/{PASSWORD}/tasks/{flask_id}')
    return response.json()

def get_statistic(flask_id):
    response = requests.get(f'http://127.0.0.1:5000/{PASSWORD}/statistic/{flask_id}')
    return response.json()