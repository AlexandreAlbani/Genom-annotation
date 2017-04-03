#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


HelpMessage = """

Projet -- view gene found on genom

ARGUMENTS :
  
 input genom
	genom file name in fasta format
	WARNING : only the first sequence is considered

 input gene
	gene file name in fasta format
	WARNING : only the first sequence is considered

 5' end of gene locus

 3' end of gene locus

"""


def read_fasta (file) :

	"""
	entrée : fichier au format fasta
	sortie : première séquence du fichier

	"""
	
	f = open(file, "r")

	seq = ""

	l = f.readline().rstrip('\n')
	l = f.readline().rstrip('\n')

	while not (l == "" or (len(l) > 0 and l[0] == '>')) :

		seq += l
		
		l = f.readline().rstrip('\n')

	f.close()
	
	return seq


if len(sys.argv) < 4 :
	sys.exit(HelpMessage)

file = sys.argv[1]
seq = read_fasta (file)

file = sys.argv[2]
gene = read_fasta (file)

debut = int(sys.argv[3]) - 1
fin = int(sys.argv[4]) - 1

if debut > fin :

	debut = len(seq) - debut - 1
	fin = len(seq) - fin - 1

extension = 10

if debut < extension :
	begin = 0
else:
	begin = debut - extension	

if debut + extension > len(seq) :
	end = len(seq) - 1
else:
	end = fin + extension

motif = seq[begin : end]

ext1 = ""
if debut < extension :
	for i in range(debut) :
		ext1 += '.'
else:
	for i in range(extension) :
		ext1 += '.'

ext2 = ""
if debut + extension > len(seq):
	for i in range(len(seq) - debut) :
		ext2 += '.'
else:
	for i in range(extension - 1) :
		ext2 += '.'

gene = ext1 + gene + ext2

d = 0
diff = ""

if len(motif) < len(gene) :
	for i in range(len(motif)) :
		if gene[i] != motif[i] and gene[i] != '.' :
			d += 1
			diff += '* '
		else :
			diff += '  '
	
else:
	for i in range(len(gene)) :
		if gene[i] != motif[i] and gene[i] != '.' :
			d += 1
			diff += '* '
		else :
			diff += '  '

window = 50
n = int (len(motif) / window)

k = 0
while k < n :

	Gene = ""
	for i in gene[k * window : (k+1) * window] :
		Gene += i + ' '

	Motif = ""
	for i in motif[k * window : (k+1) * window] :
		Motif += i + ' '

	print "\n", Motif, "\n", Gene, "\n", diff[k * window * 2 : (k+1) * window * 2]

	k += 1

	
Gene = ""
for i in gene[k * window : -1] :
	Gene += i + ' '

Motif = ""
for i in motif[k * window : -1] :
	Motif += i + ' '

print "\n", Motif, "\n", Gene, "\n", diff[k * window * 2 : -1]

print "\n number of mismatchs :", d, "\n"
