import logging
import os

from delogger import SlackHandler

dummy_url = 'dummy.url'
dummy_token = 'dummy.token'


def test_normal():
    logger = logging.getLogger('normal')
    logger.setLevel(logging.DEBUG)

    slack_handler = SlackHandler(url=dummy_url, channel='#dummy')
    slack_handler.setLevel(logging.DEBUG)
    logger.addHandler(slack_handler)

    logger.debug('normal test')


def test_url_env():
    url_env = SlackHandler.URL_ENV
    os.environ[url_env] = dummy_url

    SlackHandler(channel='#dummy')


def test_url_env_error():
    url_env = SlackHandler.URL_ENV
    if os.environ.get(url_env, None):
        del os.environ[url_env]

    try:
        SlackHandler(channel='#dummy')

    except ValueError as e:
        pass
    else:
        assert False


def test_token():
    logger = logging.getLogger('normal')
    logger.setLevel(logging.DEBUG)

    slack_handler = SlackHandler(token=dummy_token, channel='#dummy')

    assert slack_handler.url == SlackHandler.POST_MESSAGE_URL


def test_token_env():
    token_env = SlackHandler.TOKEN_ENV
    os.environ[token_env] = dummy_token

    slack_handler = SlackHandler(channel='#dummy')

    assert slack_handler.url == SlackHandler.POST_MESSAGE_URL


def token_error():
    url_env = SlackHandler.URL_ENV
    token_env = SlackHandler.TOKEN_ENV

    if os.environ.get(url_env, None):
        del os.environ[url_env]

    if os.environ.get(token_env, None):
        del os.environ[token_env]

    logger = logging.getLogger('error')
    logger.setLevel(logging.DEBUG)

    try:
        SlackHandler()

    except ValueError as e:
        pass
    else:
        assert False

    logger.debug('error test')
