import os

import pandas as pd
import pdfkit


def convert_csv_to_excel(file_path):
    """
    Converts the csv file to an excel type of file.
    """
    csv_file = pd.read_csv(f'{file_path}.csv')
    excel_file = pd.ExcelWriter(f'{file_path}.xlsx')
    csv_file.to_excel(excel_file, index = False)
    excel_file.save()


def convert_csv_to_pdf(file_path):
    """
    Converts the csv file to html and then to a pdf type of file.
    """    
    csv_file = pd.read_csv(f'{file_path}.csv')
    csv_file.to_html((f'{file_path}.html'))
    pdfkit.from_file(f'{file_path}.html', f'{file_path}.pdf')

    os.remove(f'{file_path}.html')