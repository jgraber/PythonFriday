# Example from https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
from celery import Celery
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery('tasks', backend='db+sqlite:///./celery.db', broker='amqp://guest@localhost//')
app.control.rate_limit('tasks.add', '1/m')
# app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    logger.critical(f"{x} + {y}")
    return x + y

@app.task
def reverse(text):
    return text[::-1]

if __name__ == '__main__':
    app.worker_main()