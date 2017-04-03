#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


HelpMessage = """

Projet -- annotate genom with a referenced gene
  
ARGUMENTS :
  
 input genom
	genom file name in fasta format
	WARNING : only the first sequence is considered
		    
 input gene
	gene file name in fasta format
	WARNING : only the first sequence is considered

 homology threshold
	default value : 0.8

"""

dico_format = {'a' : 'A', 'c' : 'C', 'g' : 'G', 't' :'T', ' ' : '', '\r' : ''}

seuil = 0.8


def read_file (file) :

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


def formatage (motif) :

	"""
	entrée : séquence
	sortie : séquence formatée

	"""

	m = ""
	
	for i in motif :

		if i in dico_format.values() :
			m += i

		else :
			m += dico_format[i]

	return m



def alike (subseq, motif) :

	"""
	entrée : 2 séquences de même longueur
	sortie : similiarité de séquence

	"""

	s = 0
	for i in range(len(motif)) :
		if motif[i] == subseq[i] :
			s += 1

	return float(s) / len(motif)


def align (seq, motif) :

	"""
	séqeunce, séquence de plus courte longueur
	liste des indices de la grande séquence qui font correspondre une certaine similarité entre une sous-séquence et la petite séquence 

	"""

	indices = []
	
	for i in range(len(seq) - len(motif) + 1) :
		subseq = seq[i : i + len(motif)]
		s = alike (subseq, motif)

		if s > seuil :
			indices.append(i+1)

	return indices


if len(sys.argv) < 3 :
	sys.exit(HelpMessage)

file_seq = sys.argv[1]
file_motif = sys.argv[2]

if len(sys.argv) == 4 :
	seuil = float(sys.argv[3])
	if seuil < 0 :
		seuil = 0
	elif seuil >= 1 :
		seuil = 0.999

seq = read_file (file_seq)
motif = read_file (file_motif)

seq = formatage (seq)
motif = formatage (motif)

if len(motif) <= len(seq) :

	print "\n\n genom length :", len(seq),"\n\n gene length :", len(motif)

	indices = align (seq, motif)
	print "\n\n gene location(s) :\n"
	for i in indices :
		print i, "-" , i + len(motif) - 1

	for i in range(len(indices)) :
		indices[i] = len(seq) - indices[i]

	print "\n\n reverse gene location(s) :\n"
	for i in indices :
		print i + 1, "-" ,i - len(motif) + 2
	print "\n"

else :
	print "\n length gene too long \n"
