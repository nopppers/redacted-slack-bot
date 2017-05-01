import os
import json
import logging

from pprint import pprint

from flask import Flask, request
from slackclient import SlackClient

# Comma separated list of scopes as specified here: https://api.slack.com/docs/oauth-scopes
# Since this is a Custom Bot, 'bot' gives us access to a lot: https://api.slack.com/bot-users#api_usage
REQUIRED_SCOPES = "bot" 

app = Flask(__name__)

log = logging.getLogger(__name__)

config = {}

@app.route("/auth", methods=["GET"])
def pre_auth():
	return '''
		<a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
			<img src="https://api.slack.com/img/sign_in_with_slack.png" />
		</a>
	'''.format(REQUIRED_SCOPES, config["clientID"])

if __name__ == "__main__":
	with open('config.json') as configFile:
		config = json.load(configFile)

	log.info("Starting redacted-slack-bot with client id %s", config["clientID"])
	app.run()
