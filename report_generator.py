import os
import smtplib
import datetime as dt
from email.message import EmailMessage

from psycopg2 import sql

from db_connection import get_psql_conn


EMAIL_ADDRESS = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def extract_report_to_csv(start_date, end_date, file_path):
    """
    Saving results from the database in a csv file, according to the given date range.
    The function returns the final path of the file in order to convert it (pdf or excel).
    """
    today = dt.date.today()
    file_path = f'{file_path}/report_{today}'
    
    with get_psql_conn() as conn:
        cur = conn.cursor()
        sql_statement = """COPY(
            SELECT app.start_time::date as "Date of appointment", 
                   app.test_kind as "Kind of test (pcr/antigen)", 
                   loc.name as "Test location",
            sum(case when tr.result_time is not null then 1 end) as "Number of taken tests",
            sum(case when tr.result_time is null then 1 end) as "Number of not taken tests"
            FROM test_results tr
            RIGHT OUTER JOIN appointments app
            ON tr.appointment_id=app.id
            INNER JOIN locations loc
            ON app.location_id=loc.id
            WHERE app.start_time::date between {start_date} AND {end_date}
            GROUP BY app.start_time::date, app.test_kind, loc.name
            ORDER BY app.start_time::date
        )TO STDOUT WITH CSV HEADER"""
        
        sql_query = sql.SQL(sql_statement).format(start_date=sql.Literal(start_date), end_date=sql.Literal(end_date))
        
        with open(f'{file_path}.csv', "w") as file:
            cur.copy_expert(sql_query, file)
    
    return file_path


def body_email(**kwargs):
    """
    Prepares the body of the email depending on the kind of message.
    Message can be error type or the normal message with the excel file attached.
    """
    if 'error' in kwargs.keys():
        msg = EmailMessage()
        msg['Subject'] = 'Error Report'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg.set_content(
            f'An error has occured concerning the report for the period {kwargs["start_date"]} - {kwargs["end_date"]}\n\n{kwargs["error"]}'
        )
        return msg
        
    msg = EmailMessage()
    msg['Subject'] = 'Weekly covid-tests report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f'You can find attached the report for the period {kwargs["start_date"]} - {kwargs["end_date"]}')

    with open(f'{kwargs["file_path"]}.xlsx', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    return msg

def send_email(body):
    """
    By receiving the suitable body, sends the email.
    """
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(body)