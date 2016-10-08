
import requests
import base64
import click
import configparser
import time

DEFAULT_CONFIG = 'config.ini'

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

#count = 15 is to mimic default GET search/tweets behaviour
def get_tweets(search, session, count = 15, since_id = 0, lang = None):

    params = {'q' : search, 'since_id' : since_id, 'count' : count}

    if lang != None:
        params['lang'] = lang

    r = session.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            params = params,
    )    
        
    r.raise_for_status()

    return r.json()

def print_tweet(tweet):
    text = tweet['text']
    user_name = tweet['user']['name']
    time = tweet['created_at']
    rt = tweet['retweet_count']
    fw = tweet['favorite_count']
    hashtags = tweet['entities']['hashtags']
    mentions = tweet['entities']['user_mentions']

    shift = 0

    for hashtag in hashtags:
        styled_text = click.style('#' + hashtag['text'], fg = 'blue')
        text = text[:(hashtag['indices'][0] + shift)] + styled_text + text[(hashtag['indices'][1] + shift):]
        shift = shift + len(styled_text) - (len(hashtag['text'])  + 1)

    shift = 0
    for mention in mentions:
        styled_text = click.style('@' + mention['screen_name'], fg = 'cyan')
        text = text[:(mention['indices'][0] + shift)] + styled_text + text[(mention['indices'][1] + shift):]
        shift = shift + len(styled_text) - (len(mention['screen_name']) + 1)

    click.echo('------')
    click.secho('ID: {}'.format(tweet['id']), fg = 'green')
    click.secho('@{}'.format(user_name), fg = 'blue', bold = True, nl = False)
    click.secho(' {}'.format(time), fg = 'magenta')
    click.echo(text)
    click.echo('Retweets: {}, Likes: {}'.format(rt, fw))

    click.echo('------')


@click.command()
#@click.option('--search', help = 'Searched string', prompt = 'Enter searched string')
@click.argument('searched_string')
@click.option('--config', '-c',  help = 'Path to custom config file', default = DEFAULT_CONFIG)
@click.option('--count', '-n', help = 'Number of initialy displayed tweets', default = 5)
@click.option('--interval', '-i', help = 'How often ask for new tweets (pause between requests in seconds)', default = 1)
@click.option('--lang', '-l', help = 'Restrict search to given language (usning lang parameter in GET search/tweets)', default = None)
@click.option('--clear/--no-clear', help = 'Clears screen after every get request', default = False)
@click.option('--retweets/--no-retweets', help = 'Show retweets in feed?', default = True)
def twitter_wall(searched_string, config, count, interval, lang, clear, retweets):
   
    config_file = configparser.ConfigParser()
    config_file.read(config)

    session = twitter_session(config_file['twitter']['key'], config_file['twitter']['secret'])

    last_id = 0

    #first we get desired number (set by --count option) of tweets
    tweets = get_tweets(searched_string, session, count = count, lang = lang)
    
    while True:

        for tweet in tweets['statuses']:
            
            if (retweets == False and not ('retweeted_status' in tweet)) or (retweets == True):
                print_tweet(tweet)
                print()

            if tweet['id'] > last_id:
                last_id = tweet['id']
        
        if clear == True:
            click.clear()

        #then we get any number of new tweets
        tweets = get_tweets(searched_string, session, since_id = last_id, lang = lang)
        time.sleep(interval)

if __name__ == '__main__':
    twitter_wall()    
