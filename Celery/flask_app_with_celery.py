import os
import sys
import flask
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from celery_task import prepare

app = flask.Flask(__name__)

@app.route('/task/<int:num>')
def create_task(num):
    id = prepare.delay(num)
    return str(id)

if(__name__ == "__main__"):
    app.run()
