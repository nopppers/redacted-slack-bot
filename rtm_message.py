import json
import config

AT_BOT = ""

def init(botID = None):
    if not botID:
        botID = config.get()["slackBotID"]
    global AT_BOT
    AT_BOT = '<@' + botID + '>'

# Wraps an incoming RTM message
class IncomingRTMMessage(object):
    def __init__(self, messageStr):
        self.message = messageStr

        # Is the message really a message sent by a user, or is it something else like a status update?
        self.isUserMessage = self.message["type"] == 'message'

        self.channel = self.message["channel"] if self.isUserMessage else None

        # Is the message directed at the bot?
        self.isDirectedAtBot = self.isUserMessage and \
                               AT_BOT in self.message["text"]


