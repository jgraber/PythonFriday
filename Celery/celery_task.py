import time
from celery import Celery
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery('tasks', broker='amqp://guest@localhost//')
app.control.rate_limit('celery_task.prepare', '1/m')

@app.task
def prepare(order_id):
    time.sleep(5) # simulate work
    logger.info(f"order #{order_id} prepared")

if __name__ == '__main__':
    app.worker_main()