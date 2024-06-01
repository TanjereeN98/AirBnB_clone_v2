#!/usr/bin/python3
"""script to fetch states list from storage"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


states = storage.all(State)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display list of states"""
    return render_template('7-states_list.html', states)


@app.teardown_appcontext
def tear_down(issue):
    """close the session after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
