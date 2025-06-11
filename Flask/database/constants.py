import json
import os
from dotenv import load_dotenv


with open('Flask/data/tasks.json', encoding='utf-8') as json_file:
    TASKS = json.load(json_file)

PASSWORD = 'E7X2A9M*P5L3E0!'

load_dotenv('Flask/data/.env')
API_KEY = os.getenv('API_KEY')

ICONS = {
    'bicycle': '<i class="fa-solid fa-bicycle"></i>',
    'swimming': '<i class="fa-solid fa-water"></i>',
    'running': '<i class="fa-solid fa-person-running"></i>',
    'walking': '<i class="fa-solid fa-person-walking"></i>',
    'other': '<i class="fa-solid fa-fire-flame-curved"></i>'
}