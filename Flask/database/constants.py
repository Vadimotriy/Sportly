import json

def read_json(path='Flask/data/tasks.json'):
    with open(path) as json_file:
        data = json.load(json_file)

    return data


PASSWORD = 'E7X2A9M*P5L3E0!'
