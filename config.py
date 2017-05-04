import json

# Dictionary containing the values in config.json
config = {}


def init(configFilepath = 'config.json'):
    global config
    with open(configFilepath) as configFile:
        config = json.load(configFile)


def get():
    return config