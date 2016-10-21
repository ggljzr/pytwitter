# pytwitter
Simple application for displaying tweets containing string given by parameter. In console mode application fetches desired number of tweets and then periodicaly checks for any new tweets. In web mode it runs a web frontend writen in Flask. Frontend is live at http://ggljzr.pythonanywhere.com.

Application was created as part of Python course (https://github.com/cvut/MI-PYT, in Czech).

Link to PyPi(testing) package: https://testpypi.python.org/pypi/pytwitter.


## Requirements
* Python3
* click
* requests
* Flask

##Usage

You need to have a Twitter account and create a new app at https://apps.twitter.com/.

Then you need to create config.ini file containing Twitter API key and secret. Application looks
for default config file in ~/.config/pytwitter/config.ini.

```
#create default directory for config
mkdir -p ~/.config/pytwitter/
#copy example config in place
cp config.ini.example ~/.config/pytwitter/config.ini
```

When you have config.ini in place, you just have to fill in API key and secret instead of placeholders.

Alternatively you can use --config option to specify path to any custom config file (in web or console mode).

```
pytwitter web --config /path/to/your/config.ini
```


### Console mode

```
#shows available options
pytwitter console --help
```

```
#starts fetching tweets containing '#python' in an infinte loop
#(quit with ctrl + c)
pytwitter console '#python'
```

![Screen](screen.png)


### Web mode

```
pytwitter web
```

Runs Flask embedded web server in debug mode. Web frontend will be available on [localhost:5000](http://localhost:5000). Note that this should be used only for debugging purposes. When deploying in production you should use webserver like nginx or Apache and gateway interface like wsgi to serve the app.

Frontend itself just displays tweets fetched by [GET search/tweets](https://dev.twitter.com/rest/reference/get/search/tweets) Twitter API call. Query can be submitted via URL:

```
#fetches tweets with 'python' without retweets
http://localhost:5000/search/?query=python

#fetches tweets with 'python', with retweets
http://localhost:5000/search/?query=python&retweets=on
```

