# twitter-wall
Command line application for displaying tweets containing string given by parameter. Application fetches desired number of tweets and then periodacily checks for any new tweets. Application was created as part of Python course (https://github.com/cvut/MI-PYT, in Czech).

## Requirements
* Python3
* click
* requests

##Usage

Fill in credentials in config.ini. You need to have a Twitter account and create a new app at https://apps.twitter.com/.

```
#shows available options
python3 twitterwall.py --help
```

```
#starts fetching tweets containing '#python' in an infinte loop
#(quit with ctrl + c)
python3 twitterwall.py '#python'
```


