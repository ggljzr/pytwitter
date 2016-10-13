import time
import click

from flaskapp import app, session
from utils import print_tweet, colorize
from twittersession import TwitterSession, DEFAULT_CONFIG


@click.group()
def twitter_wall():
    pass


@twitter_wall.command()
def web():
    '''
    Runs embedded Flask webserver in debug mode
    This is for debugging purposes only!
    For production use interface like wsgi to serve app with normal web server (like nginx)
    '''
    app.run(debug=True)


@twitter_wall.command()
@click.argument('searched_string')
@click.option(
    '--config',
    '-c',
    help='Path to custom config file',
    default=DEFAULT_CONFIG)
@click.option(
    '--count', '-n', help='Number of initialy displayed tweets', default=5)
@click.option(
    '--interval',
    '-i',
    help='How often ask for new tweets (pause between requests in seconds)',
    default=1)
@click.option(
    '--lang',
    '-l',
    help='Restrict search to given language (using lang parameter in GET search/tweets)',
    default=None)
@click.option(
    '--clear/--no-clear',
    help='Clears screen after every get request',
    default=False)
@click.option(
    '--retweets/--no-retweets', help='Show retweets in feed?', default=True)
def console(searched_string, config, count, interval, lang, clear, retweets):

    session = TwitterSession(config_path=config)

    last_id = 0

    #first we get desired number (set by --count option) of tweets
    tweets = session.get_tweets(searched_string, count=count, lang=lang)

    while True:

        for tweet in tweets:

            if (retweets == False and not ('retweeted_status' in tweet)) or (
                    retweets == True):
                print_tweet(tweet)
                print()

            if tweet['id'] > last_id:
                last_id = tweet['id']

        if clear == True:
            click.clear()

        #then we get any number of new tweets
        tweets = session.get_tweets(
            searched_string, since_id=last_id, lang=lang)
        time.sleep(interval)


if __name__ == '__main__':
    twitter_wall()
