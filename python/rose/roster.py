import xlrd
import datetime
from matplotlib import pyplot as plt


class Rosters:
    def __init__(self, filename) -> None:
        workbook = xlrd.open_workbook(filename)
        self.worksheet = workbook.sheet_by_index(0)

    def print(self, row_offset, col_offset):
        col_offset = col_offset * 5
        row_offset = 6 + row_offset * 4 + row_offset * 25
        for row in range(row_offset, row_offset+25):
            for col in range(col_offset, col_offset+4):
                # Print the cell values with tab space
                print(self.worksheet.cell_value(row, col), end='\t')
            print('')

    def list(self, row_offset, col_offset):
        roster = []

        col_offset = col_offset * 5
        row_offset = 6 + row_offset * 4 + row_offset * 25
        for row in range(row_offset, row_offset+25):
            roster.append({
                'Created': datetime.datetime.now(),
                'Role': self.worksheet.cell_value(row, col_offset+0),
                'Name': self.worksheet.cell_value(row, col_offset+1),
                'Team': self.worksheet.cell_value(row, col_offset+2),
                'Cost': self.worksheet.cell_value(row, col_offset+3)
            })
        return roster