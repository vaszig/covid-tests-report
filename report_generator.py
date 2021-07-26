import os
import smtplib
import datetime as dt
from email.message import EmailMessage

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
        sql_query = (
                "SELECT app.start_time, app.test_kind, loc.name, "
                "sum(case when tr.result_time is not null then 1 end) as number_of_tests, "
                "sum(case when tr.result_time is null then 1 end) as tests_not_taken "
                "FROM test_results tr "
                "RIGHT OUTER JOIN appointments app "
                "ON tr.appointment_id=app.id "
                "INNER JOIN locations loc "
                "ON app.location_id=loc.id "
                f"WHERE app.start_time BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:00' "
                "GROUP BY app.start_time, app.test_kind, loc.name "
                "ORDER BY app.start_time"
        )
    
        with open(f'{file_path}.csv', "w") as file:
            cur.copy_expert(f'COPY ({sql_query}) TO STDOUT WITH CSV HEADER', file)
    
    return file_path


def send_email(converted_file, start_date, end_date):
    """
    Defines all the necessary information for sending the report by an email.
    The email is sent with the excel file as an attachment.
    """
    msg = EmailMessage()
    msg['Subject'] = 'Weekly covid-tests report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f'You can find attached the report for the period {start_date} - {end_date}')

    with open(converted_file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
