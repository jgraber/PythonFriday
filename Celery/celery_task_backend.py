import time
from celery import Celery
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')

@app.task(ignore_result=False)
def prepare(order_id):
    time.sleep(10) # simulate work
    logger.info(f"order #{order_id} prepared")
    return f"#{order_id}"

if __name__ == '__main__':
    app.worker_main()