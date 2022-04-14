# Example from https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
from celery import Celery
import logging

app = Celery('tasks', backend='db+sqlite:///./celery.db', broker='amqp://guest@localhost//')
# app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task(bind=True)
def add(x, y):
    logging.critical(f"{x} + {y}")
    return x + y

if __name__ == '__main__':
    app.worker_main()