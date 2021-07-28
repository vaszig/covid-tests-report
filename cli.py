import argparse
import datetime as dt
import sys
import re
from pathlib import Path

from report_generator import extract_report_to_csv, body_email, send_email
from file_conversions import convert_csv_to_excel


def read_input_args():
    """
    Parsing positional and optional arguments from CLI.
    """
    parser = argparse.ArgumentParser(description='fetch the covid-tests results based on the given date range')

    parser.add_argument('dates', metavar='dates', help='enter the date range (yyyy-mm-dd yyyy-mm-dd)', nargs=2)
    parser.add_argument('path', metavar='path', help='enter the absolut path to which the csv file will be saved')
    parser.add_argument('-toexcel', '--exportexcel', action='store_true', help='exports the report to an excel file in the specified path')
    parser.add_argument('-eexcel', '--emailexcelto', action='store', help='sends the excel report via email')

    args = parser.parse_args()
    return args


def path_is_valid(path): 
    """
    Checking if the given path from the user exists.
    """
    if Path(path).is_dir():
        return True
    return False


def are_dates_valid(start_date, end_date):
    """
    Checking if the given dates (from date range) are in the proper format and in the right order.
    """
    try:
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return False
    
    if start_date > end_date:
        return False 
    return True


def email_is_valid(email):
    """
    Checking if the given string is a valid email format.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.match(regex, email)):
        return False
    return True


def args_are_valid(args, dates, path):
    """
    Checks if the parsed arguments are valid. It returns True if they are or the appropriate error message if not. 
    """
    errors = {
        'export': 'Error: email can be sent by passing only -eexcel argument.',
        'dates': 'Error: the dates are not correct. The format should be yyyy-mm-dd and starting date before ending date.',
        'path': 'Error: path does not exist.',
        'email': 'Error: wrong type of email.'
    }

    if args.exportexcel and args.emailexcelto:
        return False, errors['export']

    if not are_dates_valid(*dates):
        return False, errors['dates']

    if not path_is_valid(path):
        return False, errors['path']
    
    if args.emailexcelto:
        if not email_is_valid(args.emailexcelto):
            return False, errors['email']
    
    return True, None


if __name__ == '__main__':
    
    args = read_input_args()
    dates = vars(args).get('dates')
    path = vars(args).get('path')
    
    are_valid, errors = args_are_valid(args, dates, path)
    if errors:
        print(errors)
        sys.exit()

    file_path = extract_report_to_csv(dates[0], dates[1], path)

    # check if any optional arguments have been passed
    if args.exportexcel:
        file_path = extract_report_to_csv(dates[0], dates[1], path)
        convert_csv_to_excel(file_path)

    if args.emailexcelto:
        convert_csv_to_excel(file_path)
        body = body_email(file_path=file_path, start_date=dates[0], end_date=dates[1])
        send_email(body)