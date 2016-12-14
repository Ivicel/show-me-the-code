#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys, os
from openpyxl import load_workbook


def to_xml(file, output='numbers.xml'):
	if not file.endswith('xlsx') and not file.endswith('xls'):
		raise TypeError('Not a valid file')
	workbook = load_workbook(file)
	first_worksheet_name = workbook.get_sheet_names()[0]
	ws = workbook[first_worksheet_name]
	numbers = ET.Element('numbers')
	for r in ws.rows:
		row = ET.SubElement(numbers, 'row')
		for cell in r:
			ele = ET.SubElement(row, 'number')
			ele.text = "{value}".format(value=cell.value)
	root = ET.Element('root')		
	root.append(numbers)
	tree = ET.ElementTree(root)
	with open(output, 'wb') as f:
		f.write(b'<? xml version="1.0" encoding="UTF-8" ?>')
		tree.write(f, encoding='utf-8')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise SystemExit('Usage: %s filename' % sys.argv[0])
	to_xml(sys.argv[1])