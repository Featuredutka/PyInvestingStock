import investpy
import xlrd
import pandas as pd
from openpyxl import load_workbook, Workbook

path_to_file = '/Users/ash/Desktop/SP500.xls'
path_to_output = '/Users/ash/Desktop/test.xlsx'

book = xlrd.open_workbook(path_to_file)  # Getting local stocks names for loop
sheet = book.sheet_by_name('SP500')
reiter = 0

for col in range(sheet.nrows):  # Loop to get number of none-empty cells
    names = sheet.cell(col, 0)
    if names.value != xlrd.empty_cell.value:
        reiter = reiter + 1

data = [sheet.cell_value(r, 2) for r in range(1, reiter)]

wb = Workbook()  # Creating workbook for results
ws = wb.active
wb.save(path_to_output)

book = load_workbook(path_to_output)  # Working with output file without overwriting it within loop
writer = pd.ExcelWriter(path_to_output, engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

i = 0  # Loop iterator
progress = 0
for stock in data:  # Loop getting dividends by stock name using investpy funcs
    try:
        stock_info = investpy.stocks.get_stock_dividends(stock, country='united states')
        stock_info.insert(0, "Name", stock, True)
        stock_info = stock_info.iloc[:8]

        if i == 0:
            stock_info.to_excel(writer, "Sheet", startrow=i, header=True, index=False)
            writer.save()
            i = i + 10
        else:
            stock_info.to_excel(writer, "Sheet", startrow=i, header=False, index=False)
            writer.save()
            i = i + 9
        progress = progress + 1
        print(progress, '/505', ' - ', stock, ' - DATA FOUND')
    except:  # If there is no data provided - write 'NO DATA' to every info cell
        failuremessage = {'Name': [stock],
                          'Data1': ['NO DATA'],
                          'Data2': ['NO DATA'],
                          'Data3': ['NO DATA'],
                          'Data4': ['NO DATA'],
                          'Data5': ['NO DATA']
                          }

        df = pd.DataFrame(failuremessage)
        df.to_excel(writer, "Sheet", startrow=i, header=False, index=False)
        writer.save()

        i = i + 2
        progress = progress + 1
        print(progress, '/505', ' - ', stock, ' - DATA NOT FOUND')
        continue
