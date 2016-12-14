#!/usr/bin/env python3
import xlsxwriter


students = {
    "1": ["张三", 150, 120, 100],
    "2": ["李四", 90, 99, 95],
    "3": ["王五", 60, 66, 68]
}

workbook = xlsxwriter.Workbook('student.xlsx')
worksheet = workbook.add_worksheet()
row, column = 0, 0
for i in sorted(students.keys()):
	worksheet.write(row, column, i)
	for student in students[i]:
		column += 1
		worksheet.write(row, column, student)
	row += 1
	column = 0
workbook.close()