import pytest
import betamax
import os

from betamax.cassette import cassette

from pytwitter.twittersession import TwitterSession


#blatantly copied from https://betamax.readthedocs.io/en/latest/configuring.html#filtering-sensitive-data
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
    #test connection/api availability
    ping = os.system('ping -c 1 twitter.com')

    record = pytest.config.getoption('--record')

    if 'AUTH_FILE' in os.environ and ping == 0 and record:
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
    betamax_session.headers.update({'Accept-Encoding': 'identity'})
    return TwitterSession(
        key=AUTH['key'], secret=AUTH['secret'], session=betamax_session)


@pytest.fixture
def testapp(betamax_session):
    from pytwitter.flaskapp import app
    betamax_session.headers.update({'Accept-Encoding': 'identity'})
    app.session = TwitterSession(
        key=AUTH['key'], secret=AUTH['secret'], session=betamax_session)
    app.config['testing'] = True
    return app.test_client()


def test_config_error():
    with pytest.raises(KeyError) as e:
        TwitterSession.parse_config('/some/fake/config')


@pytest.mark.parametrize('tweet_num', [1, 15, 20])
def test_get_tweets(client, tweet_num):
    tweets = client.get_tweets('#python', count=tweet_num)
    assert len(tweets) == tweet_num
    assert '#python' in tweets[0]['text'].lower()


def test_index(testapp):
    assert 'pytwitter' in testapp.get('/').data.decode('utf-8')


def test_tweets(testapp):
    assert '#python' in testapp.get(
        '/search/?query=%23python&retweets=on').data.decode('utf-8')


def test_empty_query(testapp):
    assert 'No tweets' in testapp.get('/search/?query=').data.decode('utf-8')
