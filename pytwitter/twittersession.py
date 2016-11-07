import configparser
import base64
import sys

from os.path import expanduser

import requests

DEFAULT_CONFIG = '{}/.config/pytwitter/config.ini'.format(expanduser('~'))


class TwitterSession:
    """
    **Class for accessing twitter**
   

    It creates and keeps session to fetch tweets. Betamax sessions are
    also supported (you can pass session to constructor).
    """
    
    @staticmethod
    def create_twitter_session(api_key, api_secret, session=None):
        """
        Method for initializing new Twitter session.

        ``api_key`` -- usualy loaded from config.ini
        ``api_secret`` -- usualy loaded from config.ini
        ``session`` ( = ``None``) -- optional argument for passing Betamax session
        """
        session = session or requests.Session()
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
    def parse_config(config_path=DEFAULT_CONFIG):
        """
        Method for parsing config.ini file for Twitter API key and secret.
        """
        cfg = configparser.ConfigParser()
        cfg.read(config_path)

        try:
            key = cfg['twitter']['key']
            secret = cfg['twitter']['secret']
        except KeyError as e:
            print('Config file is missing or containing errors.')
            if config_path == DEFAULT_CONFIG:
                print('Default config file should be placed in ~/.config/pytwitter/config.ini.')
                print('Alternatively you could use -c/--config option to specify custom config file.')

            print('\nFor correct config file format check out config.ini.example and README')
            print('\nException: ')
            raise e

        return {'key' : key, 'secret' : secret}

    def __init__(self, key, secret, session=None):
        self.session = TwitterSession.create_twitter_session(
            key, secret, session)

    @classmethod
    def init_from_file(cls, config_path=DEFAULT_CONFIG, session=None):
        """
        Initializes new instance of TwitterSession from file given
        by ``config_path`` parameter.
        """
        cfg = TwitterSession.parse_config(config_path)
        return cls(key=cfg['key'], secret=cfg['secret'])


    #count = 15 is to mimic default GET search/tweets behaviour
    def get_tweets(self, search, count=15, since_id=0, lang=None):
        """
        Returns desired number of tweets containing searched string.

        ``search`` -- searched string
        ``count`` -- maximum number of returned tweets
        ``since_id`` ( = 0) -- get only tweets posted since tweet with this id was posted
        ``lang`` ( = ``None``) -- specify desired tweet language (best effort according to Twitter API docs)
        """
        params = {'q': search, 'since_id': since_id, 'count': count}

        if lang != None:
            params['lang'] = lang

        r = self.session.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            params=params, )

        r.raise_for_status()

        return r.json()['statuses']
