import os
import json
import logging
import time

import pprint

# from flask import Flask, request
from slackclient import SlackClient

# Comma separated list of scopes as specified here: https://api.slack.com/docs/oauth-scopes
# Since this is a Custom Bot, 'bot' gives us access to a lot: https://api.slack.com/bot-users#api_usage
REQUIRED_SCOPES = "bot" 
BOT_ID = "B564YBKLY"

# app = Flask(__name__)

log = logging.getLogger(__name__)

# Dictionary containing the values in config.json
config = {}

# Slack Client API object
slack = {}


# Thrown when an API call fails
class APIException(Exception):
    pass


# Performs an API call without raising errors
def unsafe_call(method, **kwargs):
    log.info("Performing API call %s", method)
    return slack.api_call(method, **kwargs)


# Performs an API call
# Raises an APIException if the call fails
def call(method, **kwargs):
    result = unsafe_call(method, **kwargs)
    if result["ok"] != True:
        exception = APIException('"ok" was false: {0}'.format(pprint.format(result)))
        raise exception
    else:
        log.info("API call succeeded.")
        return result


# Entry point
if __name__ == "__main__":
    with open('config.json') as configFile:
        config = json.load(configFile)

    log.info("Starting redacted-slack-bot")
    slack = SlackClient(config["slackToken"])

    result = call("users.list", channel="#random", text="test", as_user=True)
    pprint.pprint(result)

    #if slack.rtm_connect():
    #    while True:
    #        print(slack.rtm_read())
    #        time.sleep(1)

    # What's next?
    # Make it join channels
    # Make it react to @mentions
    # Make it react to direct messages?
    # Check out Discourse API (reference wisemonk)

#   app.run()
