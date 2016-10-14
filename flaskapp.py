from flask import Flask, render_template, request
from twittersession import TwitterSession

from jinja2 import Markup
from utils import colorize, time_filter

app = Flask(__name__)
#this could probably be elswhere
session = TwitterSession()


@app.route('/')
def hello():
    return render_template('index.html', tweets=None, retweets=True)

@app.route('/search/')
def display_tweets():   
    query = request.args.get('query')
    tweets = None

    retweets = False

    if query:
        tweets = session.get_tweets(query, count=25)

    if request.args.get('retweets'):
        retweets = True

    if retweets == False:
        tweets = [tweet for tweet in tweets if 'retweeted_status' not in tweet]

    return render_template('index.html', tweets=tweets, query=query, retweets=retweets)

def html_url_wrap(url):
    return '<a href="{}">{}</a>'.format(url['expanded_url'],url['url'])

def html_hashtag_wrap(hashtag):
    return '<a href="/search/?query=%23{}" class="hashtag">#{}</a>'.format(hashtag['text'], hashtag['text'])

def html_mention_wrap(mention):
    return '<a href="https://twitter.com/{}" target="_blank" class="mention">@{}</a>'.format(mention['screen_name'], mention['screen_name'])


@app.template_filter('colorize')
def colorize_html(tweet):
    text = colorize(tweet, html_hashtag_wrap, html_mention_wrap, html_url_wrap)
    return Markup(text)

@app.template_filter('time')
def time_filter_html(time):
    return time_filter(time)

if __name__ == '__main__':
    app.run(debug=True)
