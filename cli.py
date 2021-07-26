import argparse
import datetime as dt
import sys
import re
from pathlib import Path


def read_input_args():
    """
    Parsing positional and optional arguments from CLI.
    """
    parser = argparse.ArgumentParser(description='fetch the covid-tests results based on the given date range')

    parser.add_argument('dates', metavar='dates', help='enter the date range (yyyy-mm-dd yyyy-mm-dd)', nargs=2)
    parser.add_argument('path', metavar='path', help='enter the absolut path to which the csv file will be saved')
    parser.add_argument('-topdf', '--exportpdf', action='store_true', help='exports the report to a pdf file in the specified path')
    parser.add_argument('-toexcel', '--exportexcel', action='store_true', help='exports the report to an excel file in the specified path')
    parser.add_argument('-eexcel', '--emailexcelto', action='store', help='sends the excel report via email')
    parser.add_argument('-epdf', '--emailpdfto', action='store', help='sends the pdf report via email')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    
    args = read_input_args()
