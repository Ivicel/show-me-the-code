import xml.etree.ElementTree as ET
from openpyxl import load_workbook
import sys


def to_xml(file, output='city.xml'):
	if not file.endswith('xlsx') and not file.endswith('xls'):
		raise TypeError('Not a valid file')
	workbook = load_workbook(file)
	first_worksheet_name = workbook.get_sheet_names()[0]
	ws = workbook[first_worksheet_name]
	doc_string = '<?xml version="1.0" encoding="UTF-8"?><root><cities>'
	for row in ws.rows:
		doc_string += '<city>'
		for cell, element in list(zip(row, ['id', 'city_name'])):
			doc_string += '<{tag}>{value}</{tag}>'.format(tag=element, value=cell.value)
		doc_string += '</city>'
	doc_string += '</cities></root>'
	root = ET.fromstring(doc_string)
	tree = ET.ElementTree(root)
	with open(output, 'wb') as f:
		f.write(b'<? xml version="1.0" encoding="UTF-8" ?>')
		tree.write(f, encoding='utf-8')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise SystemExit('Usage: %s filename' % sys.argv[0])
	to_xml(sys.argv[1])