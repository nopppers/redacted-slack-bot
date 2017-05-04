import json

AT_BOT = ""

def init(botID):
    AT_BOT = '<@' + botID + '>'

# Wraps an incoming RTM message
class IncomingRTMMessage(object):
    def __init__(self, messageStr):
        self.message = json.load(messageStr)

        # Is the message really a message sent by a user, or is it something else like a status update?
        self.isUserMessage = self.message["type"] == 'message'

        # Is the message directed at the bot?
        self.isDirectedAtBot = self.isUserMessage and \
                               AT_BOT in self.message["text"]


