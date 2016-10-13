from flask import Flask, render_template, request, escape
from twittersession import TwitterSession

import jinja2

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

def url_wrap(url):
    return '<a href="{}">{}</a>'.format(url['expanded_url'],url['url'])

def hashtag_wrap(hashtag):
    return '<span class="hashtag">#{}</span>'.format(hashtag['text'])

def mention_wrap(mention):
    return '<span class="mention">@{}</span>'.format(mention['screen_name'])

def colorize(tweet, hashtag_wrap, mention_wrap, url_wrap):

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
 
@app.template_filter('colorize')
def colorize_html(tweet):
    text = colorize(tweet, hashtag_wrap, mention_wrap, url_wrap)
    return jinja2.Markup(text)
    
if __name__ == '__main__':
    app.run(debug=True)
