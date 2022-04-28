import time
from celery import Celery
app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def prepare(order_id):
    time.sleep(5) # simulate work
    print(f"order #{order_id} prepared")

if __name__ == '__main__':
    app.worker_main()