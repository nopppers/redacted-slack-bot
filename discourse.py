
import requests
import config
import python_glue
import json
from apiexception import APIException, DiscourseAPIException

baseUrl = ""

def init():
    global baseUrl
    baseUrl = config.get()["discourseAPIURL"]

def add_auth_info(dict, discourseUser):
    dict["api_key"] = config.get()["discourseTokens"][discourseUser];
    dict["api_username"] = discourseUser;

def validate_response(response):
    if not response.ok:
        raise DiscourseAPIException(
            ("Received HTTP response code {0}\n" +
             "Response text: {1}").format(response.status_code, response.text),
            response.status_code,
            response.json())
    return response.json()

def api_call(endpoint, verb, discourseUser = None, **kwargs):
    requestDict = kwargs
    if discourseUser is not None:
        add_auth_info(requestDict, discourseUser)

    requestUrl = baseUrl + endpoint
    do_request = getattr(requests, verb)
    response = do_request(requestUrl, data=requestDict)

    return validate_response(response)

def get_category_id(categoryName):
    return None

def create_topic(discourseUser,
                 title,
                 firstPostContent,
                 categoryName=None,
                 creationDate=None):
    return api_call(
        "posts",
        "post",
        discourseUser=discourseUser,
        title=title,
        raw=firstPostContent,
        category=get_category_id(categoryName),
        creationDate=creationDate
    )
