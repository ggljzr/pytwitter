import pytest

import pytwitter.utils as utils

test_tweet = {
        'id' : 123456789,
        'id_str' : '123456789',
        'user' : {'name' : 'USERR', 'screen_name' : 'loluser'},
        'entities' : {
                'hashtags' : [
                    {'text': 'mock', 'indices' : [14, 19]},
                    {'text' : 'python', 'indices' : [26, 33]},
                    {'text': 'betamax', 'indices' : [40, 48]},
                    {'text' : 'lol' ,'indices' : [49, 53]},
                    ],
                'urls' : [
                ],
                'user_mentions':[
                    {'name' : 'user_a', 'indices' : [0,5], 'screen_name' : 'usra'},
                    {'name' : 'user_b', 'indices' : [34,39], 'screen_name' : 'usrb'},
                ],
            },
        'text' : '@usra This is #mock tweet #python @usrb #betamax #lol',
        #this is what a 'text' atribute should look like when processed with fake wrap functions
        'color_text' : '<blue>@usra</blue> This is <red>#mock</red> tweet <red>#python</red> <blue>@usrb</blue> <red>#betamax</red> <red>#lol</red>',
        'created_at' : 'Wed Aug 27 13:08:45 +0000 2008',
        'retweet_count' : 666,
        'favorite_count' : 161
        }

def test_colorize():
    def fake_wrap_url(url):
        pass

    def fake_wrap_hashtag(hashtag):
        return '<red>#{}</red>'.format(hashtag['text'])
    
    def fake_wrap_mention(mention):
        return '<blue>@{}</blue>'.format(mention['screen_name'])

    color_text = utils.colorize(test_tweet, fake_wrap_hashtag, fake_wrap_mention, fake_wrap_url)

    assert color_text == test_tweet['color_text']

def test_print_tweet(capsys):
    utils.print_tweet(test_tweet)

    out, err = capsys.readouterr()
    assert 'USERR' in out
    assert '@loluser' in out

