from variables_globales import *
from orphelins import *

import math
import random
import time
import cPickle as pickle
from noise import *


def checkwater(model):
	global blocdisponibles
	global blocsaverifierpreau,blocsdeauajoute,blocseauforce
	for block in blocsaverifierpreau:
		x, y, z = block
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key in model.world:
				if model.world[key] == blocdisponibles["WATER"]:
					if blocseauforce[key]>100:
						ext_add_block(model, block, blocdisponibles["WATER"],True)
						blocseauforce[block] = blocseauforce[key]-20
						if block in blocsaverifierpreau:
							blocsaverifierpreau.remove(block)
	if len(blocsaverifierpreau)>20:
		while len(blocsaverifierpreau)>20:
			del blocsaverifierpreau[0]
	for block in blocsdeauajoute:
		x, y, z = block
		entourage =0
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key in model.world:
				entourage = entourage +1
				if model.world[key] == blocdisponibles["WATER"]:
					if blocseauforce[key]>0:
						blocseauforce[block] = blocseauforce[key]
		if entourage <5:
			del blocseauforce[block]
			ext_remove_block(model,block,True)
			blocsdeauajoute.remove(block)
	if len(blocsdeauajoute)>20:
		while len(blocsdeauajoute)>20:
			del blocsdeauajoute[0]



def checkarbres(model,boiscoupe):
	global dicoarbresfeuillages,dicoarbrestroncs,arbreattaque
#	print "j'y suis"
	print boiscoupe
	for elt in boiscoupe:
#		print "ccc"
		for arbres in dicoarbrestroncs:
			if elt in dicoarbrestroncs[arbres]:
				arbreattaque.append(arbres)
	boiscoupe = []
	for arbres in arbreattaque:
		for blocs in dicoarbresfeuillages[arbres]:
			if blocs in model.world :
				ext_remove_block(model, blocs,True)
#		print "suprime"
		for blocs in dicoarbrestroncs[arbres]:
			if blocs in model.world :
				ext_remove_block(model, blocs,True)
				position = detptsdechute(arbres,blocs)
				ext_add_block(model,position,blocdisponibles["TRONC"],True)
	arbreattaque = []

def detptsdechute(base,blocs):
	freq = 16.0 * octaves
	x,y,z = base
	xa,ya,za = blocs
	distance = z+(ya-y)
	hauteur = int(snoise3( x/ freq, distance/ freq,graine, octaves,persistance) * 14.0 + 15.0) + 1
	return(x,hauteur,distance)

"""
def bloceauacote(model,bloc):
	if not (bloc[0],bloc[1]-1,bloc[2]) in model:
		return (bloc[0],bloc[1]-1,bloc[2])
	if (not (bloc[0]-1,bloc[1]-1,bloc[2]-1) in model):
		return (bloc[0]-1,bloc[1]-1,bloc[2]-1)
	if (not (bloc[0]-1,bloc[1]-1,bloc[2]) in model) :
		return (bloc[0]-1,bloc[1]-1,bloc[2])
	if (not (bloc[0]-1,bloc[1]-1,bloc[2]+1) in model): 
		return (bloc[0]-1,bloc[1]-1,bloc[2]+1)
	if (not (bloc[0],bloc[1]-1,bloc[2]-1) in model):
		return (bloc[0],bloc[1]-1,bloc[2]-1)
	if (not (bloc[0],bloc[1]-1,bloc[2]+1) in model) :
		return (bloc[0],bloc[1]-1,bloc[2]+1
	if (not (bloc[0]+1,bloc[1]-1,bloc[2]-1) in model):
		return (bloc[0]+1,bloc[1]-1,bloc[2]-1)
	if (not (bloc[0]+1,bloc[1]-1,bloc[2]) in model):
		return (bloc[0]+1,bloc[1]-1,bloc[2])
	if (not (bloc[0]+1,bloc[1]-1,bloc[2]+1) in model):
		return (bloc[0]+1,bloc[1]-1,bloc[2]+1)
	if (not (bloc[0]-1,bloc[1],bloc[2]-1) in model):
		return (bloc[0]-1,bloc[1],bloc[2]-1)
	if (not (bloc[0]-1,bloc[1],bloc[2]) in model) :
		return (bloc[0]-1,bloc[1],bloc[2])
	if (not (bloc[0]-1,bloc[1],bloc[2]+1) in model): 
		return (bloc[0]-1,bloc[1],bloc[2]+1)
	if (not (bloc[0],bloc[1],bloc[2]-1) in model):
		return (bloc[0],bloc[1],bloc[2]-1)
	if (not (bloc[0],bloc[1],bloc[2]+1) in model) :
		return (bloc[0],bloc[1],bloc[2]+1
	if (not (bloc[0]+1,bloc[1],bloc[2]-1) in model):
		return (bloc[0]+1,bloc[1],bloc[2]-1)
	if (not (bloc[0]+1,bloc[1],bloc[2]) in model):
		return (bloc[0]+1,bloc[1],bloc[2])
	if (not (bloc[0]+1,bloc[1],bloc[2]+1) in model):
		return (bloc[0]+1,bloc[1],bloc[2]+1)
	return None
"""







