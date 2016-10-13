from flask import Flask, render_template
from twittersession import TwitterSession

app = Flask(__name__)
#this could probably be elswhere
session = TwitterSession()


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
