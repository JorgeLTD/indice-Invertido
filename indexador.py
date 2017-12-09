from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from unidecode import unidecode
from collections import Counter
from sys import exit
import re
import os
import argparse


parser = argparse.ArgumentParser(description="Indexador de palabras dentro de bases")
parser.add_argument('-base', dest='base', required=True, metavar='archivo', type=str, help='nombre del archivo xml base con los documentos dentro de la carpeta "bases".\n ejemplo: -base 2000.xml')
args = parser.parse_args()

texts = 0

stopwords = open('diccionarios/stopwords.txt', 'r', encoding='utf-8')
stopwords = stopwords.read().splitlines()

base_root = "bases/"

# file_path = 'bases/2001.xml'
base_filename = args.base
file_path = os.path.join(base_root, base_filename)

base = open(file_path, 'r')

tree = ElementTree()
tree.parse(base)
base.close()

# Iterar Documentos
base_dic = []
root = tree.getroot()
index = {}

for doc in root:
	doc_id = doc.get('id')
	print("{}...{}".format(doc_id, doc.get('url')))

	if texts == 2000:
		break
	texts = texts + 1

	text = doc.find('content').text
	text = text.casefold()
	text = text.split()

	# remover palabras vacias
	for stopword in stopwords:
		while stopword in text:
			text.remove(stopword)
	# Contar palabras
	word_frec = Counter(text)
	norma = word_frec.most_common(1)
	print("common word")
	print("{}....{}".format(norma[0][0], norma[0][1]))
	"""
	# añadir palabras al diccionario
	for word in text:
		if word not in base_dic:
			base_dic.append(word)
	"""
	# indexar palabras a documentos
	for word in word_frec.keys():
		if index.get(word):
			index[word] = index[word] + "/{},{:.2}".format(doc_id, word_frec[word] / norma[0][1])
		else:
			index[word] = "={},{:.2}".format(doc_id, word_frec[word] / norma[0][1])
	print("----------")

# Nombre de la base
file_name = os.path.splitext(os.path.basename(file_path))[0]

index_file_name = "indices/{}_index.txt".format(file_name)

index_file = open(index_file_name, 'w', encoding='utf-8')

sorted_keys = sorted(index)

for key in sorted_keys:
	# print("{}{}".format(key, index[key]))
	index_file.write("{}{}\n".format(key, index[key]))

index_file.close()
