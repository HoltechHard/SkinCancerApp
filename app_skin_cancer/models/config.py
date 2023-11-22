import json

def read_config():
    with open("models/config.json", "r") as file:
        data = json.load(file)
    return data

settings = read_config()["config"]
