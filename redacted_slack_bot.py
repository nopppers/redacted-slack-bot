import logging
import pprint
import time

# from flask import Flask, request

import config
import api
import response_system
import rtm_message

from response_system import ResponseSystem
from rtm_message import IncomingRTMMessage

# Comma separated list of scopes as specified here: https://api.slack.com/docs/oauth-scopes
# Since this is a Custom Bot, 'bot' gives us access to a lot: https://api.slack.com/bot-users#api_usage
# REQUIRED_SCOPES = "bot"

# app = Flask(__name__)

log = logging.getLogger(__name__)


# Entry point
if __name__ == "__main__":
    config.init()
    api.init()
    rtm_message.init()

    def console_printer(msg):
        pprint.pprint(msg.message)
        return True, False  # Handled, not consumed

    def default_handler(msg):
        if msg.isDirectedAtBot:
            api.send_message(msg.channel, "We have not learned such things yet.")
            return True, True
        return False, False

    responseSystem = ResponseSystem([
        (20, console_printer),
        (100, default_handler)
    ])

    log.info("Starting redacted-slack-bot")

    if api.rtm_connect():
        while True:
            messages = api.rtm_read()
            for rawMessage in messages:
                try:
                    responseSystem.handle(IncomingRTMMessage(rawMessage))
                except Exception as e:
                    errStr = "Error in response system: " + str(e)
                    log.error(errStr)
                    api.send_error(errStr)

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
