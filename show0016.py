#!/usr/bin/env python3
import json, xlsxwriter


with open('number.txt', encoding='utf-8') as fp:
	numbers = json.load(fp)
row, column = 0, 0
workbook = xlsxwriter.Workbook('numbers.xlsx')
worksheet = workbook.add_worksheet()
for i in numbers:
	for j in i:
		worksheet.write(row, column, j)
		column += 1
	row += 1
	column = 0
workbook.close()