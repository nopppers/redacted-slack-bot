import logging
import pprint
import time
import random
import functools
import json

# from flask import Flask, request

import config
import api
import discourse
import response_system
import rtm_message
import usermap
import python_glue
import traceback

from apiexception import DiscourseAPIException, APIException
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

greetingsList = [
    "hi ",
    " hi",
    "hello",
    "sup",
    " yo",
    "yo ",
    " hey",
    "hey ",
    "what's up",
    "whats up",
    "hiya",
    "heyo",
    " sup",
    "sup ",
    "holla",
    "what it do",
    "what's up",
    "whats up",
    "what's shakin",
    "whats shakin",
    "wassup",
    "whassup",
    "wassap",
    "whassap",
    "greetings",
]

def is_greeting(str):
    return any(greeting in str for greeting in greetingsList)

def is_greeting_but_not_directed_at_bot(str):
    return not rtm_message.AT_BOT.lower() in str and is_greeting(str)

def infer_command_implicit_idx(commandSearchStrs, msg):
    for command in commandSearchStrs:
        commandIdx = msg.userMessage.find(command)
        if commandIdx != -1:
            afterCommandIdx = commandIdx + len(command)
            return max(afterCommandIdx, msg.indexAfterArgs)

    return None

def infer_command_implicit_contents(commandSearchStrs, msg):
    idx = infer_command_implicit_idx(commandSearchStrs, msg)
    if idx is None:
        return None
    else:
        return msg.rawUserMessage[idx:]



# Entry point
if __name__ == "__main__":
    config.init()
    api.init()
    discourse.init()
    usermap.init()
    rtm_message.init()

    learnMemory = []

    def console_printer(msg):
        pprint.pprint(msg.message)
        return True, False  # Handled, not consumed

    def learn_memory(msg):
        if msg.isUserMessage:
            learnMemory.append(msg)
            return True, False  # Handled, not consumed
        return False, False

    def map_user(msg):
        if msg.isDirectedAtBot:
            if (infer_command_implicit_idx(["mapuser"], msg) is not None):
                for slackName, discourseName in msg.args.items():
                    try:
                        usermap.add_user(slackName, discourseName)
                        api.send_message(msg.channel, "We have added it. Thank you for your knowledge.")
                    except APIException as e:
                        api.send_message(msg.channel, str(e))
                return True, True
        return False, False


    def create_topic(msg):
        if msg.isDirectedAtBot:
            postText = infer_command_implicit_contents(["create topic", "new topic", "new post", "create post"], msg)
            if postText is not None:
                userArgKey = python_glue.find_key_in_dict(["user", "username", "person", "poster", "creator", "originator", "by", "from", "postedby", "posted_by", "post_by", "postby", "who"], msg.args)
                # If the user provided an argument for who's posting
                if (userArgKey is not None):
                    postingSlackUser = msg.args[userArgKey]
                    postingUser = usermap.slack_to_discourse(postingSlackUser)
                    # If we can't convert the username to a discourse name then maybe the username IS a discourse name!
                    if postingUser is None and usermap.is_discourse_user(postingSlackUser):
                        postingUser = postingSlackUser
                else:  # If the user didn't provide an argument for who's posting
                    postingSlackUser = "<@" + msg.userID + ">"
                    postingUser = usermap.slack_to_discourse(msg.userID)

                titleArgKey = python_glue.find_key_in_dict(["title", "name", "about", "postname", "post_name", "named", "reason", "topicname", "topic_name"], msg.args)
                topicTitle = msg.args.get(titleArgKey)

                categoryKey = python_glue.find_key_in_dict(["cat", "category", "tagged", "type", "system", "discipline", "where", "in"], msg.args)
                category = msg.args.get(categoryKey)

                dateKey = python_glue.find_key_in_dict(["date", "time", "when", "datetime", "date_time"], msg.args)
                date = msg.args.get(dateKey)

                # If we make it this far and postingUser is None then we don't have a mapping for them
                if postingUser is None:
                    api.send_message(msg.channel,
                         "Sorry, we don't know who " + postingSlackUser + " is on discourse." +
                         " Please add a user mapping by telling me to mapuser <slackID>:<discourseID>")
                    return True, True
                elif topicTitle is None:
                    api.send_message(msg.channel,
                         "We must name the topic. Please provide title:\"Topic Name\"")
                    return True, True
                else:
                    try:
                        response = discourse.create_topic(postingUser,
                                               topicTitle,
                                               postText,
                                               categoryName=category,
                                               creationDate=date)
                        api.send_message(msg.channel, "Topic created: http://discourse.mnmn.me/t/" + response["topic_slug"])
                        #api.send_code(msg.channel, pprint.pformat(response))
                    except DiscourseAPIException as e:
                        for errMsg in e.userFriendlyErrorStrList:
                            api.send_message(msg.channel, errMsg)

                    return True, True

        return False, False


    def code_test(msg):
        if msg.isDirectedAtBot and "code test" in msg.userMessage:
            api.send_code(msg.channel, SAMPLE_CODE, "cpp")
            return True, True
        return False, False

    def flavor_learn(msg):
        if msg.isDirectedAtBot and "learn" in msg.userMessage and len(learnMemory) > 0:
            api.send_message(msg.channel, random.choice(learnMemory).rawUserMessage)
            return True, True
        return False, False

    def flavor_hello(msg):
        if msg.isDirectedAtBot and is_greeting(msg.userMessage) and len(learnMemory) > 0:
            api.send_message(
                msg.channel,
                random.choice(
                    [greeting for greeting in learnMemory if is_greeting_but_not_directed_at_bot(greeting.userMessage)]
                ).rawUserMessage)
            return True, True
        return False, False

    def flavor_empty_message(msg):
        if msg.isDirectedAtBot and msg.rawUserMessage.strip() == rtm_message.AT_BOT:
            api.send_message(msg.channel, "<@" + msg.userID + ">?")
            return True, True
        return False, False

    def help(msg):
        if msg.isDirectedAtBot and "help" in msg.userMessage:
            postingSlackUser = "<@" + msg.userID + ">"
            api.send_message(msg.channel, "Hello, " + postingSlackUser + "!")
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
        (70, map_user),
        (75, create_topic),
        (80, code_test),
        (85, flavor_learn),
        (87, flavor_hello),
        (88, flavor_empty_message),
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
                    errStr += traceback.format_exc();
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
