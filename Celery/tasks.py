# Example from https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
from celery import Celery

# app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')
app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    print(f"{x} + {y}")
    return x + y

if __name__ == '__main__':
    app.worker_main()