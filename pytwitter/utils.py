from datetime import datetime

import click
from jinja2 import Markup


def time_filter(time):
    """Function to filter Twitter time format.
       It just calls ``datetime`` ``strptime`` and ``strftime``
       functions to get desired format.

       Input format -- ``%a %b %d %H:%M:%S %z %Y``
       Output format -- ``%H:%M:%S %d/%m/%Y``
    """
    dt = datetime.strptime(time, '%a %b %d %H:%M:%S %z %Y')
    return dt.strftime('%H:%M:%S %d/%m/%Y')


def url_wrap(url):
    """Url wrap function using ``click.style()`` (ANSI colors) for wrapping."""
    return click.style(url['url'], underline=True, fg='yellow')


def hashtag_wrap(hashtag):
    """Hashtag wrap function using ``click.style()`` (ANSI colors) for wrapping."""
    return click.style('#' + hashtag['text'], fg='blue')


def mention_wrap(mention):
    """Mention wrap function using ``click.style()`` (ANSI colors) for wrapping."""
    return click.style('@' + mention['screen_name'], fg='cyan')

def colorize(tweet, hashtag_wrap, mention_wrap, url_wrap):
    """
    Used to wrap entities within tweet text with desired tags to
    specify for example color output or html markup.

    ``tweet`` -- Tweet entity obtained with ``TwitterSession.get_tweets()``
    
    ``hashtag_wrap``, ``mention_wrap``, ``url_wrap`` -- functions for wrapping entities

    For example:
    
    ..code::
        
        
        def hashtag_wrap(hashtag):
            return '<span class="hashtag-span">#{}</span>'.format(hashtag['text'])
    """
    text = tweet['text']

    entities = tweet['entities']['hashtags'] + tweet['entities'][
        'user_mentions'] + tweet['entities']['urls']
    entities.sort(key=lambda e: e['indices'][0])

    shift = 0
    for entity in entities:
        text_len = 0
        styled_text = None

        if 'screen_name' in entity:
            text_len = len(entity['screen_name']) + 1
            styled_text = mention_wrap(entity)
        elif 'url' in entity:
            text_len = len(entity['url'])
            styled_text = url_wrap(entity)
        else:
            text_len = len(entity['text']) + 1
            styled_text = hashtag_wrap(entity)

        text = text[:(entity['indices'][0] + shift)] + styled_text + text[(
            entity['indices'][1] + shift):]
        shift = shift + len(styled_text) - (text_len)

    return text


def print_tweet(tweet):
    """
    Function to print tweet entity from ``TwitterSession.get_tweets()`` on stdout.
    Uses ``click.echo()`` and ``click.style()`` functions for colorized output.
    """
    text = colorize(tweet, hashtag_wrap, mention_wrap, url_wrap)
    text = Markup.unescape(text)
    created_at = time_filter(tweet['created_at'])

    click.echo('------')
    click.secho('ID: {}'.format(tweet['id']), fg='green')
    click.secho(tweet['user']['name'], fg='blue', bold=True, nl=False)
    click.secho(
        ' @{}'.format(tweet['user']['screen_name']),
        fg='white',
        bold=True,
        nl=False)
    click.secho(' {}'.format(created_at), fg='magenta')
    click.echo(text)
    click.echo('Retweets: {}, Likes: {}'.format(tweet['retweet_count'], tweet[
        'favorite_count']))

    click.echo('------')
