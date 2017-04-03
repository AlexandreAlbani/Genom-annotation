#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


HelpMessage = """

Projet -- view annotated genom

ARGUMENTS :
  
 input positions
	input file name with the follwoing format :
	one line per gene where each line contains : 5'end - 3'end

 input names
	input file name with the follwoing format :
	one line per gene where each line contains : gene_name
	WARNING : the order should correspond to the previous input file
	
 size genom in number of nucleotides

 window view size in number of nucleotides

"""


def read_names (file) :

	"""
	entrée : nom du fichier contenant la liste par ligne du nom des gènes
	sortie : liste du nom des gènes

	"""
	
	f = open(file, "r")

	l = f.readline().rstrip('\n')

	names = []

	while not l == "" :
	
		names.append(l)

		l = f.readline().rstrip('\n')

	f.close()

	return names


def read_positions (file_pos, file_names) :

	"""
	entrée : nom du fichier contenant la liste par ligne de la position des gènes, nom du fichier contenant la liste par ligne du nom des gènes
	sortie : liste de listes contenenat le début, le fin et le nom de chaque gène

	"""
	
	f = open(file_pos, "r")

	genes = []
	names = read_names (file_names)

	l = f.readline().rstrip('\n')

	i = 0

	while not l == "" :
		
		s = l.split('-')
		genes.append([int(s[0]) -1, int(s[1]) -1, names[i]])
	
		l = f.readline().rstrip('\n')

		i += 1

	f.close()

	return genes


def compress (strand_1, strand_2) :

	# fonction défecteuse

	"""
	entrée : brin sens annoté, brin antisens annoté
	sortie : brin sens annoté et synthétisé, brin antisens annoté et synthétisé

	"""
		
	cmp = 4
	
	fg = ""
	rg = ""
	i = 0
	while i < len(strand_1) - cmp + 1 :

		fg += strand_1[i]
		rg += strand_2[i]

		p1 = ""
		p2 = ""
		p3 = ""

		for j in range(cmp) :
			p1 += '_'
			p2 += '+'
			p3 += '-'

		print strand_2[i : i + cmp]

		if strand_1[i : i + cmp] == p1 or strand_1[i : i + cmp] == p2 or strand_1[i : i + cmp] == p3 :
			if strand_2[i : i + cmp] == p1 or strand_2[i : i + cmp] == p2 or strand_2[i : i + cmp] == p3 :

				i += cmp

			else:
				i += 1

		i += 1

	return fg, rg


if len(sys.argv) < 4 :
	sys.exit(HelpMessage)

file1 = sys.argv[1]
file2 = sys.argv[2]

genes = read_positions (file1, file2)


n = int(sys.argv[3])

forward = ['_' for i in range(n)]
reverse = ['_' for i in range(n)]

for i in range(len(genes)) :

	if genes[i][0] > n-1 :
		genes[i][0] = n-1
	elif genes[i][0] < 0 :
		genes[i][0] = 0

	if genes[i][1] > n-1 :
		genes[i][0] = n-1
	elif genes[i][1] < 0 :
		genes[i][0] = 0

	if genes[i][0] < genes[i][1] : 

		forward[genes[i][0]] = '|'
		forward[genes[i][1]] = '>'

		for j in range(genes[i][0] + 1, genes[i][1], 1) :
			forward[j] = '+'

		for k in range(len(genes[i][2])) :
			forward[genes[i][0] + k + 1] = genes[i][2][k]

	else :
		reverse[genes[i][0]] = '|'
		reverse[genes[i][1]] = '<'

		for j in range(genes[i][0] - 1, genes[i][1], -1) :
			reverse[j] = '-'

		for k in range(len(genes[i][2])) :
			reverse[genes[i][0] - len(genes[i][2]) + k] = genes[i][2][k]


fg = ""
rg = ""

for i in range(n) :
	fg += forward[i]
for i in range(n) :
	rg += reverse[i]

#fg, rg = compress (fg, rg)

window = int(sys.argv[4])

c = int (len(fg) / window)

for k in range(c) :
	print "\n", fg[k *window : (k+1) * window], "\n", rg[k * window : (k+1) * window]
print "\n", fg[(k+1) * window : -1], "\n", rg[(k+1) * window : -1]
