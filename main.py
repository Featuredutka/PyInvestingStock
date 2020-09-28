import investpy
import xlrd
import pandas as pd
from openpyxl import load_workbook, Workbook


def CheckOutputFile():  # Checking if there's a local source and output files -
    # if there are no - it will ask you once to declare paths to create them
    try:
        outputtxt = open('data.txt', 'r')
        pathsfromfile = [outputtxt.readline()[:-1], outputtxt.readline()]
        return pathsfromfile
    except:
        outputtxt = open('data.txt', 'w')
        print('Enter path to source file:')
        outputtxt.write(input() + '\n')
        print('Enter path to output file:')
        outputtxt.write(input())
        outputtxt.close()
        exit(0)


def MergeFunction(firstdataframe, seconddataframe):
    mergelist = [firstdataframe, seconddataframe]
    return pd.concat(mergelist)


paths = CheckOutputFile()  # Getting paths to necessary files
path_to_file = paths[0]
path_to_output = paths[1]

book = xlrd.open_workbook(path_to_file)  # Getting local stocks names for loop
sheet = book.sheet_by_name('SP500')
reiter = 0

for col in range(sheet.nrows):  # Loop to get number of none-empty cells
    names = sheet.cell(col, 0)
    if names.value != xlrd.empty_cell.value:
        reiter = reiter + 1

data = [sheet.cell_value(r, 2) for r in range(1, reiter)]  # Stock list
country_data = [sheet.cell_value(r, 3) for r in range(1, reiter)]  # Country list for multinational stock lists
result_dataframe = (investpy.stocks.get_stock_dividends('AAPL', country='united states')).iloc[:3]  # Shitty, but
# working part - necessary non-empty list for merging to work

wb = Workbook()  # Creating workbook for results
ws = wb.active
wb.save(path_to_output)

book = load_workbook(path_to_output)  # Working with output file without overwriting it within loop
writer = pd.ExcelWriter(path_to_output, engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

i = 0  # Loop iterators
progress = 0
countryiterator = 0

for stock in data:  # Loop getting dividends by stock name using investpy funcs
    try:
        stock_info = investpy.stocks.get_stock_dividends(stock, country=country_data[countryiterator])
        stock_info.insert(0, "Name", stock, True)
        stock_info = stock_info.iloc[:8]

        result_dataframe = MergeFunction(result_dataframe, stock_info)

        if data.index(stock) == 0:
            result_dataframe = result_dataframe.iloc[3:]

        progress = progress + 1
        print(progress, '/505', ' - ', stock, ' - DATA FOUND')
    except:  # If there is no data provided - write 'NO DATA' to every info cell
        data = {'Name': ['Nah'], 'Age': [20, 21, 19, 18]}

        data = pd.DataFrame(data)
        result_dataframe.append(pd.Series(name='NameOfNewRow'))
        print(result_dataframe)

        progress = progress + 1
        print(progress, '/505', ' - ', stock, ' - DATA NOT FOUND')
    finally:
        countryiterator = countryiterator + 1
        continue
