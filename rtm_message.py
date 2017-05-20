import config
import string_help

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
        self.isUserMessage = self.message["type"] == 'message' and "text" in self.message

        # If it is a message from a user, store what channel it came from
        self.channel = self.message["channel"] if self.isUserMessage else None

        if self.isUserMessage:
            # Is the message directed at the bot?
            self.isDirectedAtBot = AT_BOT in self.message["text"]
            # Store the message from the user
            self.userMessage = self.message["text"]
            # Store the first word of the message from the user
            self.firstWord = string_help.split_elem_or_empty_string(self.userMessage, 0)
            if self.isDirectedAtBot:
                # Store only the message that is intended for the bot (the part after AT_BOT)
                self.messageAtBot = string_help.partition_elem_or_empty_string(self.userMessage, 2, AT_BOT)
                # Store the first word of that message
                self.firstWordAtBot = string_help.split_elem_or_empty_string(self.messageAtBot, 0)

        else:
            self.isDirectedAtBot = False

