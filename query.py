from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from math import log10
import argparse
import os

parser = argparse.ArgumentParser(description="Programa para realizar consultas sobre un indice y archivo base. Si estos archivos no coinciden el resultado es inconsistente")
parser.add_argument('-base', dest='base', required=True, metavar='archivo_base.xml', type=str, help='nombre del archivo xml base con los documentos dentro de la carpeta "bases".\n ejemplo: -base 2000.xml')
parser.add_argument('-index', dest='index', required=True, metavar='archivo_indice.txt', type=str, help='nombre del archivo txt con los indices de las palabras de la base ingresada dentro de la carpete "indices".\n ejemplo: -index 2001_index.txt ')
args = parser.parse_args()

base_root = "bases/"
index_root = "indices/"

base_path = os.path.join(base_root, args.base)
index_path = os.path.join(index_root, args.index)

# Cargar documentos y obtener el numero total
base = open(base_path, 'r')

tree = ElementTree()
tree.parse(base)

base.close()

root = tree.getroot()
N = len(root)  # numero documentos

# Cargar el index

index_file = open(index_path, 'r', encoding='utf-8')

index = index_file.read().split()
index_dic = {}

for line in index:
	line = line.split('=')
	docs = line[1].split('/')
	index_dic[str(line[0])] = {}
	for doc in docs:
		value = doc.split(',')
		tmp_dic = {str(value[0]): value[1]}
		index_dic[line[0]].update(tmp_dic)

index_file.close()

while True:
	print("Ingrese su consulta:")
	query = input()
	query = query.casefold().split()

	#  ranking de los documentos
	rank = {}
	for doc in root:
		rank[doc.get('id')] = 0

	for word in query:
		if index_dic.get(word):
			idf_word = log10(N / len(index_dic[word]))
			# print(idf_word, word)
			for doc in index_dic[word]:
				tdf = float(index_dic[word][doc])
				w = tdf*idf_word
				rank[doc] = rank[doc] + w
				# print(index_dic[word][doc])

	# Busqueda documento mas relevante

	ranking_result = 0
	id_doc = []

	for doc in rank:
		if rank[doc] >= ranking_result:
			ranking_result = rank[doc]
			id_doc.append(doc)

	for doc in root:
		if doc.get('id') in id_doc:
			year = doc.find('year').text
			month = doc.find('month').text
			day = doc.find('day').text
			print("Archivo: {}\nFecha: {}/{}/{}".format(doc.get('url'), year, month, day))
			print("Doc:{} / Rank:{}\n------------".format(doc.get('id'), ranking_result))

	print("ingrese 's' para salir")
	if input() == "s":
		break
