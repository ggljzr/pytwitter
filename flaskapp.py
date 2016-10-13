from flask import Flask, render_template, request
from twittersession import TwitterSession

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


if __name__ == '__main__':
    app.run(debug=True)
