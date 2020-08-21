import investpy
import xlrd
import pandas as pd
from openpyxl import load_workbook, Workbook

book = xlrd.open_workbook('/Users/ash/Desktop/SP500.xls')  # Getting local stocks names for loop
sheet = book.sheet_by_name('SP500')
data = [sheet.cell_value(r, 2) for r in range(1, 506)]

wb = Workbook() # Creating workbook for results
ws = wb.active
wb.save('/Users/ash/Desktop/test.xlsx')

book = load_workbook('/Users/ash/Desktop/test.xlsx')  # Working with output file without overwriting it within loop
writer = pd.ExcelWriter('/Users/ash/Desktop/test.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

i = 0  # Loop iterator

# Решить проблему подписи названий акций и проблему отсутствия данных
for stock in data:
    try:

        stock_info = investpy.stocks.get_stock_dividends(stock, country='united states')
        stock_info = stock_info.iloc[:8]

        if i == 0:
            stock_info.to_excel(writer, "Sheet",  startrow=i, header=True, index=False)
            writer.save()
            i = i + 10
        else:
            stock_info.to_excel(writer, "Sheet", startrow=i, header=False, index=False)
            writer.save()
            i = i + 9

    except:
        print(stock, ' - NO DATA')
        continue


