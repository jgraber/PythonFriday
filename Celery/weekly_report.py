from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

app = Celery(broker='amqp://guest@localhost//')
app.conf.timezone = 'Europe/Zurich'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs every Monday morning at 6:00
    sender.add_periodic_task(
        crontab(hour=6, minute=0, day_of_week=1),
        make_report.s('WEEKLY_SALES'),
    )
    
@app.task
def make_report(report_type):
    logger.info(f"report created: {report_type}")