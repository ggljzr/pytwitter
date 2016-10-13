from flask import Flask, render_template, request
from twittersession import TwitterSession

from jinja2 import Markup
from utils import colorize

app = Flask(__name__)
#this could probably be elswhere
session = TwitterSession()


@app.route('/')
def hello():
    return render_template('index.html', tweets=None)

@app.route('/search/')
def display_tweets():   
    query = request.args.get('query')
    tweets = session.get_tweets(query)

    return render_template('index.html', tweets=tweets['statuses'])

def html_url_wrap(url):
    return '<a href="{}">{}</a>'.format(url['expanded_url'],url['url'])

def html_hashtag_wrap(hashtag):
    return '<span class="hashtag">#{}</span>'.format(hashtag['text'])

def html_mention_wrap(mention):
    return '<span class="mention">@{}</span>'.format(mention['screen_name'])


@app.template_filter('colorize')
def colorize_html(tweet):
    text = colorize(tweet, html_hashtag_wrap, html_mention_wrap, html_url_wrap)
    return Markup(text)
    
if __name__ == '__main__':
    app.run(debug=True)
