from tools import clean_html, add_xml, crear_bases
from os import walk
import os
import re

# Recorrer carpeta base

f = []
base_dir = os.getcwd()
pag_dir = os.path.join(base_dir, 'paginas')
page = 0
crear_bases()

for (dirpath, dirnames, filenames) in walk(pag_dir):
	f.extend(filenames)
	date = re.search('/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})', dirpath)
	if date and filenames:
		year = date.group('year')
		month = date.group('month')
		day = date.group('day')
		print("{}/{}/{}".format(day, month, year))
		for file in filenames:
			current_dir = os.path.join(pag_dir, dirpath)
			path_file = os.path.join(current_dir, file)
			print("{}...{}".format(page, path_file))
			text = clean_html(path_file)
			if text.__len__() > 0:
				add_xml(file, page, year, month, day, text)
				page = page + 1
		print("-----------------------------------")
