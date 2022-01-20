import flask
from flask import render_template
from flask import request

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

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', who=name)


@app.route('/even/<int:num>')
def even_or_odd(num):
    return render_template('number.html', number=num)


@app.route('/send', methods=['POST'])
def send():
    data = request.form
    return data

if(__name__ == "__main__"):
    app.run()