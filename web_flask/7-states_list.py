#!/usr/bin/python3
"""Python script that starts a Flask web application"""


from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    depo = storage.all(State).values()
    return render_template("7-states_list.html", depo=depo)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
