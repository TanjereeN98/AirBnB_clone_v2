#!/usr/bin/python3
"""flask web application"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    """display hello world"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    """display HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C(text):
    """display C <text>"""
    return f'C {escape(text)}'.replace('_', ' ')


@app.route('/python/')
@app.route('/python/<text>', strict_slashes=False)
def Python(text='is cool'):
    """display Python <text>"""
    return f'Python {escape(text)}'.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
