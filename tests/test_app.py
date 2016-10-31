import pytest
import betamax
import os

from betamax.cassette import cassette

from pytwitter.twittersession import TwitterSession

#https://betamax.readthedocs.io/en/latest/configuring.html#filtering-sensitive-data
def replace_tokens(interaction, current_cassette):

    if interaction.data['response']['status']['code'] != 200:
        return

    headers = interaction.data['request']['headers']
    token = headers.get('Authorization')

    if token == None:
        return

    current_cassette.placeholders.append(
        cassette.Placeholder(
            placeholder='<AUTH_TOKEN>', replace=token[0]))


with betamax.Betamax.configure() as config:
    if 'AUTH_FILE' in os.environ:
        AUTH_PATH = os.environ['AUTH_FILE']
        config.default_cassette_options['record_mode'] = 'all'
        AUTH = TwitterSession.parse_config(AUTH_PATH)
    else:
        AUTH = {'key': 'fake', 'secret': 'fake'}
        config.default_cassette_options['record_mode'] = 'none'

    config.cassette_library_dir = 'tests/cassettes'
    config.before_record(callback=replace_tokens)


@pytest.fixture
def client(betamax_session):
    key = AUTH['key']
    secret = AUTH['secret']
    return TwitterSession(key=key, secret=secret, session=betamax_session)


def test_config_error():
    with pytest.raises(KeyError) as e:
        TwitterSession.parse_config('/some/fake/config')


def test_get_tweets(client):
    tweets = client.get_tweets('#harambe')
    assert '#harambe' in tweets[0]['text'].lower()
