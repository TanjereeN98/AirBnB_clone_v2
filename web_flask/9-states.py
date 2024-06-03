#!/usr/bin/python3
"""script to fetch states list from storage"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exc):
    """close the session after each request"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """display a HTML page for states"""
    data = storage.all(State).values()
    return render_template("9-states.html", states=data)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """display a HTML page for specific state"""
    data = storage.all(State)
    notfound_flag = True
    for state in data.values():
        if state.id == id:
            state_obj = state
            notfound_flag = False
            break
    return render_template("9-states.html", id=id,
                           notfound_flag=notfound_flag, state=state_obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
