import bisect
import logging
import traceback

import api

log = logging.getLogger(__name__)


# Stores message handlers in a priority-sorted list
class ResponseSystem(object):
    def __init__(self, handlers = None):
        if not handlers:
            self.handlers = [] # Sorted list of (priority, handlerFunction)
        else:
            self.handlers = handlers

    # Adds a handler with the given priority.
    # 0 means the handler will be tried first.
    # If multiple handlers are added with the same priority, the most recently added takes precedence.
    def add_handler(self, priority, handlerFunc):
        bisect.insort_left(self.handlers, (priority, handlerFunc))

    # Tries every handler in priority order, from 0 to infinity.
    # Returns which handlers handled the message, and whether or not the message was consumed.
    # A consumed message will not be passed on to subsequent handlers.
    def handle(self, messageText):
        result = ResponseResult()

        # This loop returns early if one of the handlers consumed the message
        for priority, handler in self.handlers:
            try:
                # Unpack multiple return values into ResponseResult
                results = handler(messageText)
                if not results or len(results) != 2 or any(type(elem) is not bool for elem in results):
                    raise Exception("Handler {0} did not return correctly!\n".format(str(handler)))
                handlerResult = HandlerResult(*results)
            except Exception as e:
                errStr = "Error while attempting to handle message with handler {}: ".format(str(handler)) + str(e)
                errStr += "\n" + traceback.format_exc();
                log.error(errStr)
                api.send_error(messageText.channel, errStr)

            if handlerResult.handled:
                result.handled.append(handler)
            if handlerResult.consumed:
                result.consumed = True
                return result

        # Consumed is false
        return result


class ResponseResult(object):
    def __init__(self):
        self.handled = []
        self.consumed = False


class HandlerResult(object):
    def __init__(self, handled = False, consumed = False):
        self.handled = handled
        self.consumed = consumed

