import os
from openpyxl import Workbook, load_workbook

EXCEL_FILES_PATH = './integration/'
def create_excel_file(file_name):
    file_path = f'{EXCEL_FILES_PATH}{file_name}'
    if os.path.exists(file_path):
        print(f"File {file_name} already exists.")
        return False
    else:
        workbook = Workbook()
        workbook.save(filename=file_path)

        print(f"File {file_name} created.")
        return True

create_excel_file('test.xlsx')