import os
import json
import logging
import time

from pprint import pprint

#from flask import Flask, request
from slackclient import SlackClient

# Comma separated list of scopes as specified here: https://api.slack.com/docs/oauth-scopes
# Since this is a Custom Bot, 'bot' gives us access to a lot: https://api.slack.com/bot-users#api_usage
REQUIRED_SCOPES = "bot" 

#app = Flask(__name__)

log = logging.getLogger(__name__)

# Dictionary containing the values in config.json
config = {}

# Slack Client API object
slack = {}

def api_call(method, **kwargs):
    return slack.api_call(method, **kwargs)

if __name__ == "__main__":
    with open('config.json') as configFile:
        config = json.load(configFile)

    log.info("Starting redacted-slack-bot")
    slack = SlackClient(config["slackToken"])

    #result = api_call("chat.postMessage", channel="#random", text="test", as_user=True)
    #pprint(result)

    if slack.rtm_connect():
        while True:
            print(slack.rtm_read())
            time.sleep(1)

    # What's next?
    # api_call that raises errors if "ok" is false
    # Change its avatar
    # Make it join channels
    # Make it react to slash commands -- Does it matter if it's in the room?
    # Make it react to direct messages?
    # Check out Discourse API (reference wisemonk)

#   app.run()
