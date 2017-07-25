import config
import string_help

AT_BOT = ""
DELIM = ":"

def init(botID = None):
    if not botID:
        botID = config.get()["slackBotID"]
    global AT_BOT
    AT_BOT = '<@' + botID + '>'

def get_key_from_delim_split(str):
    trimmedElem = str.strip()
    if len(trimmedElem) > 0:

        if trimmedElem[-1] == "\"":
            quoteSplit = trimmedElem.split("\"")
            if len(quoteSplit) > 2:  # Make sure there were two quotes
                return quoteSplit[-2]

            # Fall out of the previous if, quote detection failed
            # Assume the user is a fuckup, get rid of the quote
            trimmedElem = trimmedElem[:-2]

        splitStr = trimmedElem.split()
        return splitStr[-1]

    return None

def get_val_from_delim_split(str):
    trimmedElem = str.strip()
    if len(trimmedElem) > 0:

        if trimmedElem[0] == "\"":
            quoteSplit = trimmedElem.split("\"")
            if len(quoteSplit) > 2:  # Make sure there were two quotes
                return quoteSplit[1]

            # Fall out of the previous if, quote detection failed
            # Assume the user is a fuckup, get rid of the quote
            trimmedElem = trimmedElem[1:]

        splitStr = trimmedElem.split()
        return splitStr[0]

    return None

def get_kvps(messageStr):
    dict = {}
    delimSplit = messageStr.split(DELIM)
    lastValidKey = None
    lastValidVal = None

    if len(delimSplit) > 0:
        key = get_key_from_delim_split(delimSplit[0])

    for i in range(1, len(delimSplit) - 1):
        val = get_val_from_delim_split(delimSplit[i])
        nextKey = get_key_from_delim_split(delimSplit[i])

        if key is not None and val is not None:
            dict[key] = val
            lastValidKey = key
            lastValidVal = val

        key = nextKey

    val = get_val_from_delim_split(delimSplit[len(delimSplit) - 1])
    if key is not None and val is not None:
        dict[key] = val
        lastValidKey = key
        lastValidVal = val

    indexAfterLastKVP = None;
    if lastValidVal is not None:
        indexAfterLastKVP = messageStr.rfind(lastValidVal) + len(lastValidVal)

    return dict, indexAfterLastKVP


# Wraps an incoming RTM message
class IncomingRTMMessage(object):
    def __init__(self, messageDict):
        # Original API message dict
        self.message = messageDict

        # Is the message really a message sent by a user, or is it something else like a status update?
        self.isUserMessage = self.message["type"] == 'message' and "text" in self.message

        # If it is a message from a user, store what channel it came from
        self.channel = self.message["channel"] if self.isUserMessage else None

        # Store the ID of the user involved
        if "user" in self.message:
            self.userID = self.message["user"]

        if self.isUserMessage:
            # Is the message directed at the bot?
            self.isDirectedAtBot = AT_BOT in self.message["text"]
            # Store the message from the user
            self.rawUserMessage = self.message["text"]
            self.userMessage = self.message["text"].lower()
            # Store the first word of the message from the user
            self.firstWord = string_help.split_elem_or_empty_string(self.userMessage, 0)
            if self.isDirectedAtBot:
                # Store only the message that is intended for the bot (the part after AT_BOT)
                self.messageAtBot = string_help.partition_elem_or_empty_string(self.userMessage, 2, AT_BOT)
                # Store the first word of that message
                self.firstWordAtBot = string_help.split_elem_or_empty_string(self.messageAtBot, 0)

            # Store any arguments present
            self.rawArgs, self.indexAfterArgs = get_kvps(self.rawUserMessage)
            self.args = {k.lower(): v for (k, v) in self.rawArgs.items()}

            if self.indexAfterArgs is None:
                self.indexAfterArgs = 0

        else:
            self.isDirectedAtBot = False
