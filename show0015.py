#!/usr/bin/env python3
import xlsxwriter, json


fp = open('city.txt', encoding='utf-8')
cities = json.load(fp)
fp.close()
workbook = xlsxwriter.Workbook('city.xlsx')
worksheet = workbook.add_worksheet()
row, column = 0, 0
for i in sorted(cities.keys()):
	worksheet.write(row, column, i)
	column += 1
	worksheet.write(row, column, cities[i])
	row += 1
	column = 0
workbook.close()