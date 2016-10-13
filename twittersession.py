import configparser
import base64

import requests

DEFAULT_CONFIG = 'config.ini'


class TwitterSession:
    @staticmethod
    def create_twitter_session(api_key, api_secret):
        session = requests.Session()
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }

        r = session.post(
            'https://api.twitter.com/oauth2/token',
            headers=headers,
            data={'grant_type': 'client_credentials'})

        r.raise_for_status()

        bearer_token = r.json()['access_token']

        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth
        return session

    @staticmethod
    def parse_config(config_path):
        config_file = configparser.ConfigParser()
        config_file.read(config_path)

        return config_file

    def __init__(self, config_path=DEFAULT_CONFIG):
        cfg = TwitterSession.parse_config(config_path)
        self.session = TwitterSession.create_twitter_session(
            cfg['twitter']['key'], cfg['twitter']['secret'])

    #count = 15 is to mimic default GET search/tweets behaviour
    def get_tweets(self, search, count=15, since_id=0, lang=None):

        params = {'q': search, 'since_id': since_id, 'count': count}

        if lang != None:
            params['lang'] = lang

        r = self.session.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            params=params, )

        r.raise_for_status()

        return r.json()
