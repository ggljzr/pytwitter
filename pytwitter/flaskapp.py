from flask import Flask, render_template, request

from jinja2 import Markup

from .utils import colorize, time_filter

app = Flask(__name__)

@app.route('/')
def hello():
    """ Displays empty index.html (for '/' flask app route)"""
    return render_template('index.html', tweets=None, retweets=True)

@app.route('/search/')
def display_tweets():
    """
    Fetches and displays tweets.
    Used in '/search/' flask app route.
    Searched query is passed with ?q=query parameter.
    """
    query = request.args.get('query')
    tweets = None

    retweets = False

    if query:
        tweets = app.session.get_tweets(query, count=25)

    if request.args.get('retweets'):
        retweets = True

    if retweets == False and tweets:
        tweets = [tweet for tweet in tweets if 'retweeted_status' not in tweet]

    return render_template('index.html', tweets=tweets, query=query, retweets=retweets)

def html_url_wrap(url):
    """Html ``utils.colorize()`` wrap for url entity."""
    return '<a href="{}">{}</a>'.format(url['expanded_url'],url['url'])

def html_hashtag_wrap(hashtag):
    """Html ``utils.colorize()`` wrap for hashtag entity."""
    return '<a href="/search/?query=%23{}" class="hashtag">#{}</a>'.format(hashtag['text'], hashtag['text'])

def html_mention_wrap(mention):
    """Html ``utils.colorize()`` wrap for mention entity."""
    return '<a href="https://twitter.com/{}" target="_blank" class="mention">@{}</a>'.format(mention['screen_name'], mention['screen_name'])


@app.template_filter('colorize')
def colorize_html(tweet):
    """ 
    Wraper for ``utils.colorize()`` function using html markup.
    Used as a filter in ``jinja`` template.
    """
    text = colorize(tweet, html_hashtag_wrap, html_mention_wrap, html_url_wrap)
    return Markup(text)

@app.template_filter('time')
def time_filter_html(time):
    """ 
    Wraper for ``utils.time_filter()`` function.
    Used as a filter in ``jinja`` template.
    """
    return time_filter(time)

