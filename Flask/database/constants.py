import json

def read_json(path='Flask/data/tasks.json'):
    with open(path) as json_file:
        data = json.load(json_file)

    return data


PASSWORD = 'E7X2A9M*P5L3E0!'
API_KEY = 'Bearer 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'