import json
import os
from dotenv import load_dotenv


with open('Flask/data/tasks.json', encoding='utf-8') as json_file:
    TASKS = json.load(json_file)

PASSWORD = 'E7X2A9M*P5L3E0!'

load_dotenv('Flask/data/.env')
API_KEY = os.getenv('API_KEY')