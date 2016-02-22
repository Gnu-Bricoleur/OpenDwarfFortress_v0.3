from variables_globales import *
from menu import *
from orphelins import *

import math
import random
import time

#import pygame
#from pygame.locals import *

#import cPickle as pickle

from noise import *
#from collections import deque
#from pyglet import image
#from pyglet.gl import *
#from pyglet.graphics import TextureGroup
#from pyglet.window import key, mouse


def creeZombies():
	freq = 16.0 * octaves
	global listeZombie
	global UNDEMILARGEURLONGUEURDUMONDE
	for i in range(0, random.randint(10,20)):
		x = random.randint((-UNDEMILARGEURLONGUEURDUMONDE+10),(UNDEMILARGEURLONGUEURDUMONDE-10))
		y = random.randint((-UNDEMILARGEURLONGUEURDUMONDE+10),(UNDEMILARGEURLONGUEURDUMONDE-10))
		hauteur = int(snoise3(x / freq, y / freq,graine, octaves,persistance) * 14.0 + 15.0)
		listeZombie.append([i,x,hauteur,y])


def initZombies(model):
	freq = 16.0 * octaves
	global listeZombie
	global UNDEMILARGEURLONGUEURDUMONDE
	for zombie in listeZombie:
		ext_add_block(model,(zombie[1],zombie[2],zombie[3]),blocdisponibles["ZOMBIECORP"],True)
		ext_add_block(model,(zombie[1],zombie[2]+1,zombie[3]),blocdisponibles["ZOMBIETETE"],True)




def deplacerZombies(model,positionjoueur):
	global zombies_initialise
	global listeZombie
	freq = 16.0 * octaves
	if zombies_initialise == False:
		initZombies(model)
		zombies_initialise = True
#	print positionjoueur
	for zombie in listeZombie:
		if abs(positionjoueur[0]-zombie[1])<15 and abs(positionjoueur[2]-zombie[3])<15:
			print "Attention DANGER !!"
			ancienx, ancieny,ancienz = zombie[1],zombie[3],zombie[2]
			a,b = equadedroite(zombie[1],zombie[3],positionjoueur[0],positionjoueur[2])
			if positionjoueur[0] == zombie[1]:
				zombie[1]=zombie[1]+1
				x=zombie[1]
				y=int(a*x+b)
			elif positionjoueur[0]-zombie[1]<0:
				x=zombie[1]-1
				y=int(a*x+b)
			else:
				x=zombie[1]+1
				y=int(a*x+b)
			zombie[1]=x
			zombie[3]=y
			hauteur = int(snoise3(zombie[1] / freq, zombie[3] / freq,graine, octaves,persistance) * 14.0 + 15.0)
			#evitement d'obstacle : si il y a un bloc dans le passage passe par dessus
			zombie[2] = hauteur
			if (zombie[1],hauteur,zombie[3]) in model.world and not ((zombie[1],hauteur+1,zombie[3]) in model.world) and not((zombie[1],hauteur+2,zombie[3]) in model.world ):
				ext_remove_block(model,(ancienx,ancienz,ancieny),True)
				ext_remove_block(model,(ancienx,ancienz+1,ancieny),True)
				zombie[2] =zombie[2]+1
				ext_add_block(model,(zombie[1],zombie[2],zombie[3]),blocdisponibles["ZOMBIECORP"],True)
				ext_add_block(model,(zombie[1],zombie[2]+1,zombie[3]),blocdisponibles["ZOMBIETETE"],True)
				#evitement si obsttacle en hauteur et longeur
				"""
			elif not ((zombie[1],hauteur,zombie[3]) in model.world) and not( (zombie[1],hauteur + 1,zombie[3]) in model.world):
				if ancieny-zombie[3] == 0:
					zombie
				"""
			elif not ((zombie[1],hauteur,zombie[3]) in model.world) and not ((zombie[1],hauteur + 1,zombie[3]) in model.world):
				ext_remove_block(model,(ancienx,ancienz,ancieny),True)
				ext_remove_block(model,(ancienx,ancienz + 1,ancieny),True)
				ext_add_block(model,(zombie[1],zombie[2],zombie[3]),blocdisponibles["ZOMBIECORP"],True)
				ext_add_block(model,(zombie[1],zombie[2]+1,zombie[3]),blocdisponibles["ZOMBIETETE"],True)
