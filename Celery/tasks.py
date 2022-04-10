# Example from https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y