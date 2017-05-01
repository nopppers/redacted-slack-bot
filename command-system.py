import bisect

class ResponseSystem(object):
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        bisect.insort_right(handler)

    def handle(self, messageText):
        for handler in self.handlers:
            if handler.can_handle_message(messageText):
                # Only break if the handler consumes the message
                if handler.handle_message(messageText):
                    break;


class CommandHandler(object):
    def __init__(self, priority):
        self.priority = priority

    def __int__(self):
        return self.priority

    def __lt__(self, other):
        return self.priority < other.priority

# A handler can take input as either a string or as python arguments
# A handler has a name
# Handlers can access other handlers' functions


# Or...
# A handler only takes input and turns it into arguments to a python function
#