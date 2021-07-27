import unittest
import csv
from pathlib import Path
import datetime as dt
from unittest.case import expectedFailure

from report_generator import extract_report_to_csv
from db_connection import get_psql_conn


class TestReportGenerator(unittest.TestCase):

    def test_report_generator_extracts_csv(self):
        today = dt.date.today()
        file_path = extract_report_to_csv('2021-03-01', '2021-03-01', '/tmp')
        self.assertTrue(Path(f'{file_path}.csv').is_file())
        self.assertEqual(file_path, f'/tmp/report_{today}')

    def test_report_generator_retrieves_right_data(self):
        file_path = extract_report_to_csv('2021-07-01', '2021-07-31', '/tmp')
        with open(f'{file_path}.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            
            for row in csv_reader:
                if line_count == 0:
                    columns = row
                    line_count += 1
                else:
                    line_count += 1
            
            expected_columns = ['start_time', 'test_kind', 'name', 'number_of_tests', 'tests_not_taken']
            self.assertEqual(columns, expected_columns)
            self.assertEqual(line_count, 4)

        