import datetime as dt

from db_connection import get_psql_conn


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
