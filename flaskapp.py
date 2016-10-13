from flask import Flask, render_template

import apiutils as api

app = Flask(__name__)

cfg = api.get_config()

@app.route('/')
def hello():
    return render_template('index.html')
        
if __name__ == '__main__':
    app.run(debug=True)
