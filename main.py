import investpy
import xlrd
import pandas as pd
from openpyxl import load_workbook, Workbook
from progress.bar import IncrementalBar


def CheckOutputFile():  # Checking if there's a local source and output files
    try:
        with open('data.txt', 'r') as outputtxt:
            pathsfromfile = [outputtxt.readline()[:-1], outputtxt.readline()]
        return pathsfromfile
    except:
        with open('data.txt', 'w') as outputtxt:
            print('Enter path to source file:')
            outputtxt.write(input().replace('\\', '/') + '\n')
            print('Enter path to output file:')
            outputtxt.write(input().replace('\\', '/'))
        return CheckOutputFile()

def NoDataFoundMessage(stock):
    failuremessage = {'Name': [stock],
                          'Data1': ['NO DATA'],
                          'Data2': ['NO DATA'],
                          'Data3': ['NO DATA'],
                          'Data4': ['NO DATA'],
                          'Data5': ['NO DATA']
                          }
    return failuremessage


paths = CheckOutputFile()  # Getting paths to necessary files
path_to_file = paths[0]
path_to_output = paths[1]

with xlrd.open_workbook(path_to_file) as book:  # Getting local stocks names for loop
    sheet = book.sheet_by_name('SP500')
    
cell_iterator = 0

for col in range(sheet.nrows):  # Loop to get number of none-empty cells
    names = sheet.cell(col, 0)
    if names.value != xlrd.empty_cell.value:
        cell_iterator = cell_iterator + 1

data = [sheet.cell_value(r, 2) for r in range(1, cell_iterator)]  # An array of stock short names
country_data = [sheet.cell_value(r, 3) for r in range(1, cell_iterator)]  # Country list for multinational stock lists

wb = Workbook()  # Creating workbook for results
ws = wb.active
wb.save(path_to_output)

book = load_workbook(path_to_output)  # Working with output file without overwriting it within loop
writer = pd.ExcelWriter(path_to_output, engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

i = 0  # Loop iterators
countryiterator = 0
bar = IncrementalBar('Processing', max=len(data))  # Initializing the progress bar

for stock in data:  # Loop getting dividends by stock name using investpy funcs
    try:
        stock_info = investpy.stocks.get_stock_dividends(stock, country=country_data[countryiterator])
        stock_info.insert(0, "Name", stock, True)
        stock_info = stock_info.iloc[:8]
        if i != 0:
            stock_info.to_excel(writer, "Sheet", startrow=i, header=False, index=False)
            writer.save()
            i = i + 9
        else:
            stock_info.to_excel(writer, "Sheet", startrow=i, header=True, index=False)
            writer.save()
            i = i + 10
        bar.next()
        print(' - ', stock, ' - DATA FOUND')
    except RuntimeError:  # If there is no data provided - write 'NO DATA' to every info cell
        df = pd.DataFrame(NoDataFoundMessage(stock))
        df.to_excel(writer, "Sheet", startrow=i, header=False, index=False)
        writer.save()
        i = i + 2
        bar.next()
        print(' - ', stock, ' - DATA NOT FOUND')
    except KeyboardInterrupt:  # Beautiful wrapping of keyboard interruption traceback
        print("\n#-#-# Interrupted by User #-#-#")
        exit(0)
    finally:
        countryiterator = countryiterator + 1

bar.finish()