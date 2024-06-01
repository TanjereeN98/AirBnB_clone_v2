#!/usr/bin/python3
"""flask web application"""

from flask import Flask
from markupsafe import escape
from flask import render_template

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


@app.route('/number/<int:n>', strict_slashes=False)
def Number(n):
    """display Number"""
    return f'{escape(n)} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """Display a HTML page Odd or even?"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
