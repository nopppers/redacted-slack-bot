
# Thrown when an API call fails
class APIException(Exception):
    pass

class DiscourseAPIException(Exception):
    def __init__(self, str, code, response):
        super(DiscourseAPIException, self).__init__(self, str)
        self.code = code;
        self.response = response;
        self.userFriendlyErrorStrList = response["errors"];
