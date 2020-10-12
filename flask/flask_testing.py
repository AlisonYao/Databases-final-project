# use environment: Python 3.7.0 64-bit /usr/local/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello World!'
    return render_template('flask_testing.html')

@app.route('/niceday')
def nice():
    return "it's a nice day"


if __name__ == "__main__":
    app.run('127.0.0.1', 5000)
