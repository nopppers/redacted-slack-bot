import logging
import pprint
import time

# from flask import Flask, request

import config
import api

# Comma separated list of scopes as specified here: https://api.slack.com/docs/oauth-scopes
# Since this is a Custom Bot, 'bot' gives us access to a lot: https://api.slack.com/bot-users#api_usage
# REQUIRED_SCOPES = "bot"

# app = Flask(__name__)

log = logging.getLogger(__name__)

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
    config.init()
    api.init()

    log.info("Starting redacted-slack-bot")

    if api.rtm_connect():
       while True:
           print(api.rtm_read())
           time.sleep(1)

    # Use this and find the bot user to find what the value of slackBotID should be.
    #result = call("users.list", channel="#random", text="test", as_user=True)
    #pprint.pprint(result)



    # What's next?
    # Make it join channels
    # Make it react to @mentions
    # Make it react to direct messages?
    # Check out Discourse API (reference wisemonk)

#   app.run()
