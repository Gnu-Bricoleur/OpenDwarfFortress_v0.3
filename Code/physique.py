from variables_globales import *
from orphelins import *

import math
import random
import time
import cPickle as pickle
from noise import *


def checkwater(model):
	global blocdisponibles
	global blocsaverifierpreau
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
	if len(blocsaverifierpreau)>10:
		while len(blocsaverifierpreau)>20:
			del blocsaverifierpreau[0]
	for block in blocsdeauajoute:
		x, y, z = block
		entourage =0
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key in model.world:
				entourage =entourage +1
				if model.world[key] == blocdisponibles["WATER"]:
					if blocseauforce[key]>0:
						blocseauforce[block] = blocseauforce[key]
		if entourage <11:
			del blocseauforce[block]
			ext_remove_block(model,block)
			blocsdeauajoute.remove(block)
	if len(blocsdeauajoute)>10:
		while len(blocsdeauajoute)>20:
			del blocsdeauajoute[0]




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







		
