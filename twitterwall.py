import time
import click

import apiutils as api

from flaskapp import app


def print_tweet(tweet):
    text = tweet['text']

    entities = tweet['entities']['hashtags'] + tweet['entities'][
        'user_mentions']
    entities.sort(key=lambda e: e['indices'][0])

    shift = 0
    for entity in entities:
        text_len = 0
        styled_text = None

        if 'screen_name' in entity:
            text_len = len(entity['screen_name'])
            styled_text = click.style('@' + entity['screen_name'], fg='cyan')
        else:
            text_len = len(entity['text'])
            styled_text = click.style('#' + entity['text'], fg='blue')

        text = text[:(entity['indices'][0] + shift)] + styled_text + text[(
            entity['indices'][1] + shift):]
        shift = shift + len(styled_text) - (text_len + 1)

    click.echo('------')
    click.secho('ID: {}'.format(tweet['id']), fg='green')
    click.secho(tweet['user']['name'], fg='blue', bold=True, nl=False)
    click.secho(
        ' @{}'.format(tweet['user']['screen_name']),
        fg='white',
        bold=True,
        nl=False)
    click.secho(' {}'.format(tweet['created_at']), fg='magenta')
    click.echo(text)
    click.echo('Retweets: {}, Likes: {}'.format(tweet['retweet_count'], tweet[
        'favorite_count']))

    click.echo('------')


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
    default=api.DEFAULT_CONFIG)
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

    cfg = api.get_config(config_path=config)

    session = api.twitter_session(cfg['twitter']['key'],
                                  cfg['twitter']['secret'])

    last_id = 0

    #first we get desired number (set by --count option) of tweets
    tweets = api.get_tweets(searched_string, session, count=count, lang=lang)

    while True:

        for tweet in tweets['statuses']:

            if (retweets == False and not ('retweeted_status' in tweet)) or (
                    retweets == True):
                print_tweet(tweet)
                print()

            if tweet['id'] > last_id:
                last_id = tweet['id']

        if clear == True:
            click.clear()

        #then we get any number of new tweets
        tweets = api.get_tweets(
            searched_string, session, since_id=last_id, lang=lang)
        time.sleep(interval)


if __name__ == '__main__':
    twitter_wall()
