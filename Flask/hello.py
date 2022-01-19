import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Hello worldd!"

def get_latest_tasks():
    return [
        {'id': 1, 'description': 'write post', 'done': False},
        {'id': 2, 'description': 'create examples', 'done': True},
        {'id': 3, 'description': 'simplify examples', 'done': True},
        {'id': 4, 'description': 'create images', 'done': False},
    ]


@app.route('/tasks')
def tasks():
    my_tasks = get_latest_tasks()
    return render_template('tasks.html', name='Johnny', tasks=my_tasks)

@app.route('/about')
def about():
    return render_template('about.html')

if(__name__ == "__main__"):
    app.run()