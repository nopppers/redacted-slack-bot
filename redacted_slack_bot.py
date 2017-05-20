import logging
import pprint
import time
import random

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

SAMPLE_CODE = \
"""
template <typename T>
T & maybe_deref(T &x)
{
    return x;
}

template <typename T>
T & maybe_deref(T *x)
{
    return *x;
}
"""

# Entry point
if __name__ == "__main__":
    config.init()
    api.init()
    rtm_message.init()

    learnMemory = []

    def console_printer(msg):
        pprint.pprint(msg.message)
        return True, False  # Handled, not consumed

    def learn_memory(msg):
        if msg.isUserMessage:
            learnMemory.append(msg.userMessage)
            return True, False  # Handled, not consumed
        return False, False

    def code_test(msg):
        if msg.isDirectedAtBot and "code test" in msg.userMessage:
            api.send_code(msg.channel, SAMPLE_CODE, "cpp")
            return True, True
        return False, False

    def flavor_learn(msg):
        if msg.isDirectedAtBot and "learn" in msg.userMessage and len(learnMemory) > 0:
            api.send_message(msg.channel, random.choice(learnMemory))
            return True, True
        return False, False

    def help(msg):
        if msg.isDirectedAtBot and "help" in msg.userMessage:
            api.send_message(msg.channel, "Greetings. We are not currently of much help.")
            return True, True
        return False, False

    def default_handler(msg):
        if msg.isDirectedAtBot:
            api.send_message(msg.channel, "We have not learned such things yet.")
            return True, True
        return False, False

    responseSystem = ResponseSystem([
        (20, console_printer),
        (22, learn_memory),
        (80, code_test),
        (85, flavor_learn),
        (90, help),
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
                    errStr = "Error in response system: " + str(e) + ".\n Message was: " + pprint.pformat(rawMessage)
                    log.error(errStr)
                    if "channel" in rawMessage:
                        api.send_error(rawMessage["channel"], errStr)

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
