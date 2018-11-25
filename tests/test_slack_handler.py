import json
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

    assert slack_handler.url != SlackHandler.POST_MESSAGE_URL

    logger.debug('normal test')


def test_slack_handler_dup():
    logger = logging.getLogger('slack_dup')
    logger.setLevel(logging.DEBUG)

    slack_handler = SlackHandler(url=dummy_url, channel='#dummy')
    slack_handler.setLevel(logging.DEBUG)
    logger.addHandler(slack_handler)

    slack_handler = SlackHandler(url=dummy_url, channel='#dummy')
    slack_handler.setLevel(logging.DEBUG)
    logger.addHandler(slack_handler)

    assert slack_handler.url != SlackHandler.POST_MESSAGE_URL
    assert len(logger.handlers) == 1

    logger.debug('slack handler duplication')


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

    except ValueError:
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


def test_token_error():
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

    except ValueError:
        pass
    else:
        assert False

    logger.debug('error test')


def test_make_content_with_url():
    levelno = logging.DEBUG

    slack_handler = SlackHandler(url=dummy_url, channel='#dummy')
    content = slack_handler._makeContent(levelno)

    assert type(content) is str
    content = json.loads(content)
    assert content['icon_emoji'] == slack_handler.emojis[levelno]
    assert content['username'] == slack_handler.usernames[levelno]
    assert content['channel'] == '#dummy'
    assert 'as_user' not in content
    assert 'token' not in content

    assert slack_handler.url != SlackHandler.POST_MESSAGE_URL


def test_make_content_with_token():
    levelno = logging.DEBUG

    slack_handler = SlackHandler(
        token=dummy_token,
        channel='#dummy',
        as_user=True,
    )
    content = slack_handler._makeContent(levelno)

    assert type(content) is dict
    assert 'icon_emoji' not in content
    assert 'username' not in content
    assert content['channel'] == '#dummy'
    assert content['as_user']
    assert content['token'] == dummy_token

    assert slack_handler.url == SlackHandler.POST_MESSAGE_URL


def test_params():
    slack_handler = SlackHandler(
        url=dummy_url,
        emoji='emoji',
        username='username',
    )
    content = slack_handler._makeContent(logging.INFO)
    content = json.loads(content)

    assert content['icon_emoji'] == 'emoji'
    assert content['username'] == 'username'
