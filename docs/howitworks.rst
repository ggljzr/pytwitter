How it works
============

Application uses `Twitter API <https://dev.twitter.com/overview/api>`__ to search for tweets containing queried string and then displays them via standard output or web frontend written in Flask.


Creating new Twitter session
----------------------------

.. code::
   
    from pytwitter.twittesession import TwitterSession 

    cfg = TwitterSession.parse_config('/path/to/config/file.ini')

    session = TwitterSession(cfg['key'], cfg['secret'])

    #alternatively

    session = TwitterSession.init_from_file('/path/to/config/file.ini')

Fetching tweets
---------------

.. code::
    
    #tweets containing '#python'
    tweets = session.get_new_tweets('#python')

    #new tweets containing '#python' since last query
    last_seen = tweets[0]['id']
    new_tweets = session.get_tweets('#python', since_id=last_seen)

Processing entities in tweet
----------------------------

.. testsetup::

    tweet = {
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

.. testcode::

    import pytwitter.utils as utils

    def wrap_url(url):
        return '<cyan>{}</cyan>'.format(url['url'])

    def wrap_hashtag(hashtag):
        return '<red>#{}</red>'.format(hashtag['text'])
    
    def wrap_mention(mention):
        return '<blue>@{}</blue>'.format(mention['screen_name'])


    # original tweet text:
    # @usra This is #mock tweet #python @usrb #betamax #lol
    processed_text = utils.colorize(tweet, 
                                    wrap_hashtag, 
                                    wrap_mention, 
                                    wrap_url)
    print(processed_text)

.. testoutput:: 
   
    <blue>@usra</blue> This is <red>#mock</red> tweet <red>#python</red> <blue>@usrb</blue> <red>#betamax</red> <red>#lol</red>
