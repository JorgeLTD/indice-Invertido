from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from unidecode import unidecode


def clean_html(url):
	# Leer archivo html
	html = open(url, encoding="latin1")

	soup = BeautifulSoup(html, "html.parser")

	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract()  # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)

	# borrar acentos
	# text = unidecode(text)
	"""
	# separar simbolos de palabras
	text = text.replace("(", " ( ")
	text = text.replace(")", " ) ")
	text = text.replace(":", " : ")
	text = text.replace('"', ' " ')
	text = text.replace(".", " . ")
	text = text.replace(",", " , ")
	text = text.replace("-", " - ")
	text = text.replace("", " ")
	text = text.replace("<i>", " ")
	text = text.replace("</i>", " ")
	text = text.replace("¿", "")
	text = text.replace("?", "")
	"""

	# traducir codigos
	text = text.replace('&ntilde;', 'ñ')
	text = text.replace('&aacute;', 'á')
	text = text.replace('&eacute;', 'é')
	text = text.replace('&iacute;', 'í')
	text = text.replace('&oacute;', 'ó')
	text = text.replace('&uacute;', 'ú')

	text = text.replace("(", "")
	text = text.replace(")", "")
	text = text.replace(":", " ")
	text = text.replace(";", "")
	text = text.replace('"', '')
	text = text.replace(".", "")
	text = text.replace(",", "")
	text = text.replace("-", "")
	text = text.replace("", "")
	text = text.replace("<i>", "")
	text = text.replace("</i>", "")
	text = text.replace("¿", "")
	text = text.replace("?", "")
	text = text.replace("/", "")
	text = text.replace("<b>", "")
	text = text.replace("<br>", "")
	text = text.replace("!", "")
	text = text.replace("¡", "")
	text = text.replace("'", "")
	text = text.replace("&quot;", "")
	text = text.replace(">>", "")
	text = text.replace("&lt;", "")
	text = text.replace("&gt;", "")
	text = text.replace("%", "")
	text = text.replace("$", "")
	text = text.replace("=", "")
	text = text.replace("+", "")
	text = text.replace("* ", "")

	return text


def crear_bases():
	root = Element("base")
	tree = ElementTree(root)
	tree.write("bases/1998.xml")
	tree.write("bases/1999.xml")
	tree.write("bases/2000.xml")
	tree.write("bases/2001.xml")


def add_xml(url, doc_id, year, month, day, text):
	# lee xml existente, si no exite, se rompe el programa
	file_name = "bases/{}.xml".format(year)
	file = open(file_name, 'r')
	tree = ElementTree()
	tree.parse(file)
	file.close()

	root = tree.getroot()

	doc = SubElement(root, 'document')
	doc.set('url', url)
	doc.set('id', str(doc_id))

	year_xml = SubElement(doc, 'year')
	year_xml.text = year

	month_xml = SubElement(doc, 'month')
	month_xml.text = month

	day_xml = SubElement(doc, 'day')
	day_xml.text = day

	content_xml = SubElement(doc, 'content')
	content_xml.text = text

	tree.write(file_name, encoding="utf-8")


"""
# creacion documento xml
root = Element('base')
doc = SubElement(root,'document')
year = SubElement(doc, 'year')
#TODO modificar fecha dependiente del documento
year.text = "2000"
month = SubElement(doc, 'month')
month.text = "02"
day = SubElement(doc, 'date')
day.text = "25"
content = SubElement(doc, 'content')
content.text = text

file = open("base.xml", "w")

file.write(prettify(root))
file.close()
print(prettify(root))

# print(text)

"""
