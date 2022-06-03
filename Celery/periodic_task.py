from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery(broker='amqp://guest@localhost//')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls ping('https://improveandrepeat.com') every 10 seconds.
    sender.add_periodic_task(10.0, ping.s('https://improveandrepeat.com'), name='run every 10s')

    # Calls ping('https://jgraber.ch') 10 times every 30 seconds
    # sender.add_periodic_task(30.0, ping.s('https://jgraber.ch'), expires=10)
    
    
@app.task
def ping(url):
    logger.info(f"ping {url}")