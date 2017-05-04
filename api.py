import config
import time
from slackclient import SlackClient

def init():
    global slack
    slack = SlackClient(config.get()["slackToken"])

def rtm_connect():
    return slack.rtm_connect()


def rtm_read():
    return slack.rtm_read()


def rtm_read_loop():
