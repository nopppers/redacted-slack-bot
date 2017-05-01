import os
import json
from pprint import pprint

if __name__ == "__main__":
	with open('config.json') as configFile:
		config = json.load(configFile)

	pprint(config)
