import datetime as dt

from celery import Celery
from celery.schedules import crontab

from report_generator import extract_report_to_csv, body_email,send_email
from file_conversions import convert_csv_to_excel


app = Celery('celery_tasks', broker='redis://localhost:6379/0', backend='redis://localhost')
app.conf.timezone = 'UTC'

@app.task
def send_weekly_report():
    """
    Calculates the dates for 1 week ago (Monday to Sunday) and sends the report by an email 
    depending on the date range. If an error occurs sends an email with the error.
    """
    start_date = (dt.datetime.today() - dt.timedelta(days=7)).date()
    end_date = (dt.datetime.today() - dt.timedelta(days=1)).date()

    try:
        file_path = extract_report_to_csv(start_date, end_date, '/tmp')
        convert_csv_to_excel(file_path)
        body = body_email(file_path=file_path, start_date=start_date, end_date=end_date)
        send_email(body)
    except Exception as e:
        body = body_email(error=e, start_date=start_date, end_date=end_date)
        send_email(body)
        

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'celery_tasks.send_weekly_report',
        'schedule': crontab(hour=4, minute=00, day_of_week=1),
    },
}
