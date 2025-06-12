import json
import os
from dotenv import load_dotenv


with open('Flask/data/tasks.json', encoding='utf-8') as json_file:
    TASKS = json.load(json_file)

PASSWORD = 'E7X2A9M*P5L3E0!'

load_dotenv('Flask/data/.env')
API_KEY = os.getenv('API_KEY')

ICONS = {
    'велосипед': '<i class="fa-solid fa-bicycle"></i>',
    'плавание': '<i class="fas fa-swimmer"></i>',
    'бег': '<i class="fa-solid fa-person-running"></i>',
    'ходьба': '<i class="fa-solid fa-person-walking"></i>',
    'other': '<i class="fa-solid fa-fire-flame-curved"></i>'
}

NAMES = {
    'велосипед': 'kilometre_bicycle',
    'плавание': 'kilometre_swimming',
    'бег': 'kilometres',
    'ходьба': 'kilometres',
    'пресс': 'press',
    'отжимания': 'push_up',
    'подтягивания': 'pull_up',
    'приседания': 'squats',
}