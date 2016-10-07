
import requests
import base64
import click
import configparser

def twitter_session(api_key, api_secret):
    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')
 
    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }
 
    r = session.post('https://api.twitter.com/oauth2/token',
                     headers=headers,
                     data={'grant_type': 'client_credentials'})
 
    bearer_token = r.json()['access_token']
 
    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req
 
    session.auth = bearer_auth
    return session


def get_tweets(search, config):

    session = twitter_session(config['twitter']['key'], config['twitter']['secret'])

    r = session.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            params = {'q' : str(search)},
    )

    r.raise_for_status()

    return r.json()

def print_tweet(tweet):
    text = tweet['text']
    user_name = tweet['user']['name']
    time = tweet['created_at']
    rt = tweet['retweet_count']
    fw = tweet['favorite_count']

    print('@{} {}'.format(user_name, time))
    print(text)
    print('Retweets: {}, Likes: {}'.format(rt, fw))

@click.command()
@click.option('--search', help = 'Searched string', prompt = 'Enter searched string')
def twitter_wall(search):
    config = configparser.ConfigParser()
    config.read('config.ini')

    tweets = get_tweets(search, config)

    for tweet in tweets['statuses']:
        print_tweet(tweet)
        print()

if __name__ == '__main__':
    twitter_wall()    
