
import pathlib
import json
from apiexception import APIException

import config

slackToDiscourse = {}
discourseToSlack = {}
usermapfilepath = ""

def recache():
    global discourseToSlack
    global slackToDiscourse
    discourseToSlack = {v: k for k, v in slackToDiscourse.items()}

def init():
    global usermapfilepath
    global slackToDiscourse
    global discourseToSlack

    usermapfilepath = pathlib.Path(config.get()["usermapfile"])
    if usermapfilepath.is_dir():
        raise Exception("usermapfile is a directory...")
    elif usermapfilepath.is_file():
        with usermapfilepath.open() as usermapfile:
            slackToDiscourse = json.load(usermapfile)

    recache()


def save_mappings():
    with usermapfilepath.open('w') as usermapfile:
        json.dump(slackToDiscourse, usermapfile)


def add_user(slackName, discourseName):
    if (discourseName in config.get()["discourseTokens"]):
        slackToDiscourse[slackName] = discourseName
        discourseToSlack[discourseName] = slackName
        save_mappings()
    else:
        raise APIException("We don't have a token for " + discourseName + ". Is that really a discourse username? @noppers")


def slack_to_discourse(slackName):
    return slackToDiscourse.get(slackName)


def discourse_to_slack(discourseName):
    return discourseToSlack.get(discourseName)

def is_discourse_user(username):
    return username in discourseToSlack

