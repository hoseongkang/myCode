import pandas as pd
from pandas.errors import EmptyDataError
import os
import zipfile

from openpyxl import load_workbook

def test_open_file(file_path):
    try:
        wb = load_workbook(filename=file_path)
        print("File opened successfully")
    except Exception as e:
        print(f"Error opening file: {e}")

test_open_file('C:/Temp/기준.xlsx')


def xlsx_to_csv(xlsx_file_path, csv_file_path):
    if not os.path.isfile(xlsx_file_path):
        print(f"File not found: {xlsx_file_path}")
        return
    
    try:
        # Read the Excel file
        df = pd.read_excel(xlsx_file_path, engine='openpyxl')
        # Write to CSV
        df.to_csv(csv_file_path, index=False)
        print(f"Successfully converted {xlsx_file_path} to {csv_file_path}")
    except FileNotFoundError:
        print(f"File not found: {xlsx_file_path}")
    except pd.errors.EmptyDataError:
        print(f"No data: {xlsx_file_path}")
    except zipfile.BadZipFile:
        print(f"Error: {xlsx_file_path} is not a valid zip file (not an .xlsx file)")
    except Exception as e:
        print(f"An error occurred: {e}")

xlsx_file = 'C:/Temp/기준.xlsx'  # Path to your .xlsx file
csv_file = 'C:/Temp/output.csv'     # Path where the .csv file will be saved
xlsx_to_csv(xlsx_file, csv_file)
