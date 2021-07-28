import os

import pandas as pd


def convert_csv_to_excel(file_path):
    """
    Converts the csv file to an excel type of file.
    """
    csv_file = pd.read_csv(f'{file_path}.csv')
    writer = pd.ExcelWriter(f'{file_path}.xlsx')
    csv_file.to_excel(writer, index = False, sheet_name='report')

    worksheet = writer.sheets['report']

    # adjust the width of the columns
    worksheet.set_column('A:B', 30)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:E', 30)

    writer.save()