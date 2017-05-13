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
        # Original API message dict
        self.message = messageStr

        # Is the message really a message sent by a user, or is it something else like a status update?
        self.isUserMessage = self.message["type"] == 'message'

        # If it is a message from a user, store what channel it came from
        self.channel = self.message["channel"] if self.isUserMessage else None

        # Is the message directed at the bot?
        self.isDirectedAtBot = self.isUserMessage and \
                               "text" in self.message and \
                               AT_BOT in self.message["text"]

        if self.isUserMessage:
            # Store the message from the user
            self.userMessage = self.message["text"]
            # Store the first word of the message from the user
            self.firstWord = self.userMessage.split()[0]
            if self.isDirectedAtBot:
                # Store only the message that is intended for the bot (the part after AT_BOT)
                self.messageAtBot = self.userMessage.partition(AT_BOT)[2]
                # Store the first word of that message
                self.firstWordAtBot = self.messageAtBot.split()[0]


