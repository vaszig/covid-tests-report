import os

import pandas as pd


def convert_csv_to_excel(file_path):
    """
    Converts the csv file to an excel type of file.
    """
    csv_file = pd.read_csv(f'{file_path}.csv')
    excel_file = pd.ExcelWriter(f'{file_path}.xlsx')
    csv_file.to_excel(excel_file, index = False)
    excel_file.save()
