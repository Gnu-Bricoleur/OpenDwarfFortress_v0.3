"""
Code source du jeu Open Dwarf Fortress version O.3

Code par Sylvain Migaud alias le Gnu-Bricoleur

Ce programme est sous licence libre heberge sur Github : https://github.com/Gnu-Bricoleur
Pour comprendre ce code et l'ameilorer, rendez vous sur le wiki : http://gnu-bricoleur.tuxfamily.org/dokuwiki/doku.php?id=start

Les conventions utilisees dans ce programme sont les suivantes : (mise aux normes du programme et redactions des regles en cours)
- Les noms de variables sont long compose de plusieurs mots chacun separe par des majuscules ex: hauteurDuDongeon, profondeurDuDongeon
-



"""

from Code.variables_globales import *
from Code.menu import *

import math
import random
import time

import pygame
from pygame.locals import *

import cPickle as pickle

from noise import *
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse




def cube_vertices(x, y, z, n):
	""" Return the vertices of the cube at position x, y, z with size 2*n.

	"""
	return [
		x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
		x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
		x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
		x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
	]


def object_vertices(x, y, z, n):
	""" Return the vertices of the cube at position x, y, z with size 2*n.

	"""
	return [
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
	]



def tex_coord(x, y, n=16):
	""" Return the bounding vertices of the texture square.

	"""
	m = 1.0 / n
	dx = x * m
	dy = y * m
	return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
	""" Return a list of the texture squares for the top, bottom and side.

	"""
	top = tex_coord(*top)
	bottom = tex_coord(*bottom)
	side = tex_coord(*side)
	result = []
	result.extend(top)
	result.extend(bottom)
	result.extend(side * 4)
	return result

def chargeblocs(chemindacces):
	listelignes = []
	fichier = open(chemindacces,'r')
	listelignesbrutes = fichier.readlines()
	for ligne in listelignesbrutes:
		if "#" in ligne:
			pass
		else:
			l=ligne.split(",")
			listelignes.append(l)
	fichier.close()
	for ligne in listelignes:
		blocdisponibles[ligne[0]]=tex_coords((int(ligne[1]),int(ligne[2])),(int(ligne[3]),int(ligne[4])),(int(ligne[5]),int(ligne[6])))


"""

GRASS = tex_coords((0, 15), (2, 15), (3, 15))
SAND = tex_coords((2, 14), (2, 14), (2, 14))
BRICK = tex_coords((7, 15), (7, 15), (7, 15))
STONE = tex_coords((0, 14), (0, 14), (0, 14))
WATER = tex_coords((14, 2), (14, 2), (14, 2))
STONED = tex_coords((1, 15), (1, 15), (1, 15))
BUISSON = tex_coords((5,12),(5,12),(5,12))
DIRT = tex_coords((2, 15),(2, 15),(2, 15))
FLOWER = tex_coords((12,15),(12,15),(12,15))
TRONC = tex_coords((5,14),(5,14),(4,14))
FEUILLAGE = tex_coords((5,7),(5,7),(5,7))
PNJTETE = tex_coords((6,9),(8,8),(8,8))
PNJCORP = tex_coords((6,8),(6,8),(6,8))

"""


def normalize(position):
	""" Accepts `position` of arbitrary precision and returns the block
	containing that position.

	Parameters
	----------
	position : tuple of len 3

	Returns
	-------
	block_position : tuple of ints of len 3

	"""
	x, y, z = position
	x, y, z = (int(round(x)), int(round(y)), int(round(z)))
	return (x, y, z)

def equadedroite(x1,y1,x2,y2):
	#renvois le a et le b de y=ax+b
	a=(y2-y1)/(x2-x1)
	b=y1-(a*x1)
	return a,b


def generertrajectoire(PNJ):
	#range dans un tableau la liste des coordonnes du PNJ
	freq = 16.0 * octaves
	trajectoire=[]
	trajectemp=[]
	ptsdepassage=dicoPNJ[PNJ]
	"""
	for i in range(len(ptsdepassage)-1):
		a,b=equadedroite(ptsdepassage[i][0],ptsdepassage[i][1],ptsdepassage[i+1][0],ptsdepassage[i+1][1])
		x1,y1,x2,y2=ptsdepassage[i][0],ptsdepassage[i][1],ptsdepassage[i+1][0],ptsdepassage[i+1][1]
		for x in range(x1,x2,1):
			if (int(math.floor(x)),int(math.floor(a*x+b)))in trajectemp:
				pass
			else:
				hauteur = int(snoise3(int(math.floor(x)) / freq, int(math.floor(a*x+b))/ freq,graine, octaves,persistance) * 14.0 + 15.0)
				trajectemp.append((int(math.floor(x)),int(math.floor(a*x+b))))
				trajectoire.append((int(math.floor(x)),hauteur,int(math.floor(a*x+b))))
	a,b=equadedroite(ptsdepassage[-1][0],ptsdepassage[-1][1],ptsdepassage[0][0],ptsdepassage[0][1])
	x1,y1,x2,y2=ptsdepassage[-1][0],ptsdepassage[-1][1],ptsdepassage[0][0],ptsdepassage[0][1]
	for x in range(x1,x2,1):
		if (int(math.floor(x)),int(math.floor(a*x+b)))in trajectemp:
			pass
		else:
			hauteur = int(snoise3(int(math.floor(x)) / freq, int(math.floor(a*x+b))/ freq,graine, octaves,persistance) * 14.0 + 15.0)
			trajectemp.append((int(math.floor(x)),int(math.floor(a*x+b))))
			trajectoire.append((int(math.floor(x)),hauteur,int(math.floor(a*x+b))))
	print trajectoire
	return trajectoire
	"""
	for i in range(len(ptsdepassage)-1):
		x1,y1,x2,y2=ptsdepassage[i][0],ptsdepassage[i][1],ptsdepassage[i+1][0],ptsdepassage[i+1][1]
		a,b=equadedroite(x1,y1,x2,y2)
		iterateur=x1
		while iterateur <= x2:
			carrex = int(math.floor(iterateur))
			carrey = int(math.floor(iterateur*a+b))
			if (carrex,carrey) in trajectemp:
				pass
			else:
				hauteur = int(snoise3(carrex / freq, carrey/ freq,graine, octaves,persistance) * 14.0 + 15.0)
				trajectemp.append((carrex,carrey))
				trajectoire.append((carrex,hauteur,carrey))
			iterateur=iterateur + 0.1
	x1,y1,x2,y2=ptsdepassage[-1][0],ptsdepassage[-1][1],ptsdepassage[0][0],ptsdepassage[0][1]
	a,b=equadedroite(x1,y1,x2,y2)
	iterateur=x1
	while iterateur <= x2:
		carrex = int(math.floor(iterateur))
		carrey = int(math.floor(iterateur*a+b))
		if (carrex,carrey) in trajectemp:
			pass
		else:
			hauteur = int(snoise3(carrex / freq, carrey/ freq,graine, octaves,persistance) * 14.0 + 15.0)
			trajectemp.append((carrex,carrey))
			trajectoire.append((carrex,hauteur,carrey))
		iterateur=iterateur + 0.1
	print trajectoire
	return trajectoire





def sectorize(position):
	""" Returns a tuple representing the sector for the given `position`.

	Parameters
	----------
	position : tuple of len 3

	Returns
	-------
	sector : tuple of len 3

	"""
	x, y, z = normalize(position)
	x, y, z = x / SECTOR_SIZE, y / SECTOR_SIZE, z / SECTOR_SIZE
	return (x, 0, z)




class Model(object):
	global modifsasauvegarder
	global positionpremierbloc
	global enregistrementdemodele
	global positiondebutdongeonx,positiondebutdongeony
	global dicoPNJ
	def __init__(self):

		# A Batch is a collection of vertex lists for batched rendering.
		self.batch = pyglet.graphics.Batch()

		# A TextureGroup manages an OpenGL texture.
		self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

		# A mapping from position to the texture of the block at that position.
		# This defines all the blocks that are currently in the world.
		self.world = {}

		# Same mapping as `world` but only contains blocks that are shown.
		self.shown = {}

		# carte des biomes
		self.biomes = {}
		
		# carte des points d'interets
		self.interet = {}

		# Mapping from position to a pyglet `VertextList` for all shown blocks.
		self._shown = {}

		# Mapping from sector to a list of positions inside that sector.
		self.sectors = {}

		# Simple function queue implementation. The queue is populated with
		# _show_block() and _hide_block() calls
		self.queue = deque()

		self._initialize()


	def deplacerPNJ(self,xyz,positionjoueur):
		"""
		x,y,z=positionjoueur
		dx,dy,dz = xyz
		for PNJ in dicoPNJ:
			intermediaire = dicotrajectoirePNJ[PNJ]
			if intermediaire[dicopositiondesPNJ[PNJ]] in self.shown:
				temp=dicotrajectoirePNJ[PNJ]
				if dicopositiondesPNJ[PNJ] == len(dicotrajectoirePNJ[PNJ])-2:
					self.remove_block(temp[-1])
					self.remove_block((temp[-1][0],temp[-1][1]+1,temp[-1][2]))
					dicopositiondesPNJ[PNJ] = 0
				else:
					dicopositiondesPNJ[PNJ]=dicopositiondesPNJ[PNJ]+1
					pos=dicopositiondesPNJ[PNJ]
					self.remove_block(temp[pos-1])
					self.remove_block((temp[pos-1][0],temp[pos-1][1]+1,temp[pos-1][2]))
					self.add_block(temp[pos], PNJCORP)
					self.add_block((temp[pos][0],temp[pos][1]+1,temp[pos][2]), PNJTETE)
			else:
				self.incrementerPNJ(PNJ)
		"""
		for PNJ in dicoPNJ:
			trajectoire=dicotrajectoirePNJ[PNJ]
#			print  PNJ + " : " + str(len(trajectoire)) + " : " + str(dicopositiondesPNJ[PNJ])
			if trajectoire[dicopositiondesPNJ[PNJ]] in self.shown:
				if dicopositiondesPNJ[PNJ] == len(trajectoire)-1:
					if trajectoire[-1] in self.world and (trajectoire[-1][0],trajectoire[-1][1]+1,trajectoire[-1][2]) in self.world:
						self.remove_block(trajectoire[-1])
						self.remove_block((trajectoire[-1][0],trajectoire[-1][1]+1,trajectoire[-1][2]))
					dicopositiondesPNJ[PNJ]=0
					self.add_block(trajectoire[0], blocdisponibles["PNJCORP"])
					self.add_block((trajectoire[0][0],trajectoire[0][1]+1,trajectoire[0][2]), blocdisponibles["PNJTETE"])
				else :
					pos=dicopositiondesPNJ[PNJ]
					if trajectoire[pos] in self.world and (trajectoire[pos][0],trajectoire[pos][1]+1,trajectoire[pos][2]) in self.world:
						self.remove_block(trajectoire[pos])
						self.remove_block((trajectoire[pos][0],trajectoire[pos][1]+1,trajectoire[pos][2]))
					dicopositiondesPNJ[PNJ]=dicopositiondesPNJ[PNJ]+1
					pos=dicopositiondesPNJ[PNJ]
					self.add_block(trajectoire[pos], blocdisponibles["PNJCORP"])
					self.add_block((trajectoire[pos][0],trajectoire[pos][1]+1,trajectoire[pos][2]), blocdisponibles["PNJTETE"])
			else:
				self.incrementerPNJ(PNJ)


	def incrementerPNJ(self,PNJ):
		trajectoire=dicotrajectoirePNJ[PNJ]
		if dicopositiondesPNJ[PNJ] == len(trajectoire)-1:
			dicopositiondesPNJ[PNJ]=0
		else:
			dicopositiondesPNJ[PNJ]=dicopositiondesPNJ[PNJ]+1


	def creer_monde(self):
		global mapdungeon
		global positiondebutdongeonx,positiondebutdongeony
		freq = 16.0 * octaves
		increment=0
		hauteur=0
		taillebiome=0
		indexbiome=0
		biomecourant=0
		n = UNDEMILARGEURLONGUEURDUMONDE  # 1/2 width and height of world
		s = 1  # step size
		y = 0  # initial y height
		for x in xrange(-n, n + 1, s):
			for z in xrange(-n, n + 1, s):
				# create a layer stone an grass everywhere.
				hauteur = int(snoise3(x / freq, z / freq,graine, octaves,persistance) * 14.0 + 15.0)
				if hauteur >= 20:
					for increment in xrange(0,hauteur,1):
						self.biome_montagne(x,increment,z)
				if hauteur <= 10:
					for increment in xrange(0,hauteur,1):
						self.add_block((x, increment , z), blocdisponibles["SAND"], immediate=False)
					for increment in xrange(hauteur, 10, 1):
						self.add_block((x, increment , z), blocdisponibles["WATER"], immediate=False)
				if 10 < hauteur < 20:
#                    if indexbiome == taillebiome:
#                        taillebiome = 0
#                        biomecourant =0
					if indexbiome <=taillebiome and biomecourant !=0:
						if biomecourant == 1:
							self.biome_plaine(x,hauteur,z)
							indexbiome=indexbiome+1
						elif biomecourant == 2:
							self.biome_foret(x,hauteur,z)
							indexbiome=indexbiome+1
					else :
						taillebiome,indexbiome,biomecourant=self.biome(taillebiome,indexbiome,biomecourant)
						if biomecourant == 1:
							self.biome_plaine(x,hauteur,z)
							indexbiome=indexbiome+1
						elif biomecourant == 2 :
							self.biome_foret(x,hauteur,z)
							indexbiome=indexbiome+1
					for increment in xrange(0,hauteur-1,1):
						self.add_block((x, increment , z), blocdisponibles["DIRT"], immediate=False)
#                self.add_block((x, y - 2, z), GRASS, immediate=False)
				self.add_block((x, y - 3, z), blocdisponibles["STONE"], immediate=False)
				if x in (-n, n) or z in (-n, n):
					# create outer walls.
					for dy in xrange(-2, 3):
						self.add_block((x, y + dy, z), blocdisponibles["STONE"], immediate=False)
		make_map()
		hauteurdungeon=4
		altitudedungeon=2
#		print mapdungeon
		xmax=len(mapdungeon)
		ymax=len(mapdungeon[0])
		for xdun in range(1,xmax-1):
			for ydun in range(1,ymax-1):
				if mapdungeon[xdun][ydun]==True:
					self.add_block((xdun, altitudedungeon, ydun), blocdisponibles["STONED"], immediate=False)
					self.add_block((xdun, altitudedungeon+hauteurdungeon, ydun), blocdisponibles["STONED"], immediate=False)
					for hdun in range(hauteurdungeon-1):
						self.remove_block((xdun, altitudedungeon+hdun+1, ydun),immediate=False)
				# OR est le ou non exclusif (xor pour le ou exclusif)
				elif mapdungeon[xdun+1][ydun+1]==True: 
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun-1][ydun-1]==True:
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun+1][ydun-1]==True:
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun-1][ydun+1]==True: 
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun+1][ydun]==True: 
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun-1][ydun]==True: 
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun][ydun+1]==True: 
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
				elif mapdungeon[xdun][ydun-1]==True:
					for hdun in range(hauteurdungeon):
						self.add_block((xdun, altitudedungeon+hdun, ydun), blocdisponibles["STONED"], immediate=False)
		hauteuracces = int(snoise3(positiondebutdongeonx / freq, positiondebutdongeony / freq,graine, octaves,persistance) * 14.0 + 15.0)
		for acces in range(altitudedungeon,hauteur):
			self.remove_block((positiondebutdongeonx,acces,positiondebutdongeony))
		entre=self.loadmodeleenregistre('maison')
		for elements in entre:
			self.add_block((elements[0]+positiondebutdongeonx,elements[1]+hauteuracces,elements[2]+positiondebutdongeony), entre[elements], immediate=False)


	def loadmodeleenregistre(self,nomModele):
		nom='Sauvegardes/MesModeles/'+nomModele+'.p'
		dico=pickle.load(file(nom))
		return dico

	def biome(self,taillebiome,indexbiome,biomecourant):
		if taillebiome == 0:
			taillebiome = random.randint(10000,20000)
		if biomecourant == 0:
			if random.randint(1,5) == 3:
				biomecourant = 2
			else:
				biomecourant = 1
		return taillebiome,indexbiome,biomecourant


	def biome_montagne(self,x,y,z):
		self.add_block((x, y , z), blocdisponibles["STONED"], immediate=False)
		self.biomes[(x,y,z)]='MONTAGNE'
		
	def biome_plaine(self,x,y,z):
		self.add_block((x, y-1 , z), blocdisponibles["GRASS"], immediate=False)
		if random.randint(1,250)==2:
			self.add_block((x, y , z), blocdisponibles["BUISSON"], immediate=False)
		elif random.randint(1,10)==2:
			self.add_block((x, y , z), blocdisponibles["FLOWER"], immediate=False)
		elif random.randint(1,250)==5:
			self.arbre(x, y , z)
		self.biomes[(x,y,z)]='PLAINE'
	
	def biome_foret(self,x,y,z):
		self.add_block((x, y-1 , z), blocdisponibles["GRASS"], immediate=False)
		if random.randint(1,5)==2:
			self.add_block((x, y , z), blocdisponibles["BUISSON"], immediate=False)
		elif random.randint(1,100)==2:
			self.add_block((x, y , z), blocdisponibles["FLOWER"], immediate=False)
		elif random.randint(1,25)==5:
			self.arbre(x, y , z)
		self.biomes[(x,y,z)]='FORET'


	def arbre(self,xo,yo,zo) :
#        self.add_block((x, hauteur , z), TRONC, immediate=False)
		taillearbre=random.randint(5,10)
		for i in xrange(0, taillearbre, 1):
			if taillearbre > 8:
				self.add_block((xo+1, i+yo , zo), blocdisponibles["TRONC"], immediate=False)
				self.add_block((xo+1, i+yo , zo+1), blocdisponibles["TRONC"], immediate=False)
				self.add_block((xo, i+yo , zo+1), blocdisponibles["TRONC"], immediate=False)
			self.add_block((xo, i+yo , zo), blocdisponibles["TRONC"], immediate=False)
		rayonfeuillage=random.randint(2,4)+int(taillearbre/3)
		for y in xrange(yo-rayonfeuillage+taillearbre, yo+rayonfeuillage+taillearbre, 1):
			for x in xrange(xo-rayonfeuillage,xo+rayonfeuillage , 1):
				for z in xrange(zo-rayonfeuillage,zo+rayonfeuillage , 1):
					if (y-yo)**2+(x-xo)**2+(z-zo)**2 < rayonfeuillage**2:
						self.add_block((x, y+taillearbre-3, z), blocdisponibles["FEUILLAGE"], immediate=False)
					if math.ceil((y-yo)**2+(x-xo)**2+(z-zo)**2) == rayonfeuillage**2 and random.randint(1,10)>8:
						self.add_block((x, y+taillearbre-3, z), blocdisponibles["FEUILLAGE"], immediate=False)


	"""
	def saveproxy(self):
#		picklableMethod = MethodProxy(someObj, someObj.method)
		picklableMethod = MethodProxy(Model, Model.world)
		pickle.dump( picklableMethod, open( "Sauvegardes/saveWorld.p", "wb" ) )
		pickle.dump( self.model.shown, open( "Sauvegardes/saveShown.p", "wb" ) )
		pickle.dump( self.model._shown, open( "Sauvegardes/save_Shown.p", "wb" ) )
		pickle.dump( self.model.sectors, open( "Sauvegardes/saveSectors.p", "wb" ) )
		pickle.dump( self.model.biomes, open( "Sauvegardes/saveBiomes.p", "wb" ) )
		pickle.dump( self.model.interet, open( "Sauvegardes/saveInteret.p", "wb" ) )

	"""
	def save(self):
		pickle.dump( modifsasauvegarder, open( "Sauvegardes/PartieEnCours/seauve.p", "wb" ) )
		mon_fichier = open("Sauvegardes/PartieEnCours/seed.txt", "w")
		mon_fichier.write(str(graine))
		mon_fichier.close()





	def charge(self):
		dico=pickle.load(file("Sauvegardes/PartieEnCours/seauve.p"))
		mon_fichier = open("Sauvegardes/PartieEnCours/seed.txt", "r")
		s = eval(mon_fichier.read())
		return s,dico



	def remplirdicoPNJ(self):
		nbrdePNJ = random.randint(10,20)
		nbrdeptsdepassage = random.randint(3,7)
		for iterat in range(nbrdePNJ):
			listptsdepassage=[]
			for itera in range(nbrdeptsdepassage):
				x=random.randint(-UNDEMILARGEURLONGUEURDUMONDE-5,UNDEMILARGEURLONGUEURDUMONDE-5)
				y=random.randint(-UNDEMILARGEURLONGUEURDUMONDE-5,UNDEMILARGEURLONGUEURDUMONDE-5)
				if listptsdepassage != []:
					while x == listptsdepassage[-1][0] or listptsdepassage[0][0]==x:
						x=random.randint(-UNDEMILARGEURLONGUEURDUMONDE-5,UNDEMILARGEURLONGUEURDUMONDE-5)
				listptsdepassage.append((x,y))
			dicoPNJ[iterat]=listptsdepassage





	def _initialize(self):
		""" Initialize the world by placing all the blocks.
		
		"""
		if choix == 1 :
			self.creer_monde()
		elif choix == 2:
			s,dico = self.charge()
			graine=s
			self.creer_monde()
			for elt in dico:
				if dico[elt]=="pasblocpasbloc":
					self.remove_block(elt, immediate=True)
				else:
					self.add_block(elt, dico[elt], immediate=False)
		self.remplirdicoPNJ()
		for PNJ in dicoPNJ:
			dicotrajectoirePNJ[PNJ]=generertrajectoire(PNJ)
			temp=dicotrajectoirePNJ[PNJ]
			self.add_block(temp[0], blocdisponibles["PNJCORP"], immediate=False)
			self.add_block((temp[0][0],temp[0][1]+1,temp[0][2]), blocdisponibles["PNJTETE"], immediate=False)
			dicopositiondesPNJ[PNJ]=0



#		# generate the hills randomly
#        o = n - 10
#        for _ in xrange(120):
#            a = random.randint(-o, o)  # x position of the hill
#            b = random.randint(-o, o)  # z position of the hill
#            c = -1  # base of the hill
#            h = random.randint(1, 6)  # height of the hill
#            s = random.randint(4, 8)  # 2 * s is the side length of the hill
#            d = 1  # how quickly to taper off the hills
#            t = random.choice([GRASS, SAND, BRICK])
#            for y in xrange(c, c + h):
#                for x in xrange(a - s, a + s + 1):
#                    for z in xrange(b - s, b + s + 1):
#                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
#                            continue
#                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
#                            continue
#                        self.add_block((x, y, z), t, immediate=False)
#                s -= d  # decrement side lenth so hills taper off



	def hit_test(self, position, vector, max_distance=8):
		""" Line of sight search from current position. If a block is
		intersected it is returned, along with the block previously in the line
		of sight. If no block is found, return None, None.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check visibility from.
		vector : tuple of len 3
			The line of sight vector.
		max_distance : int
			How many blocks away to search for a hit.

		"""
		m = 8
		x, y, z = position
		dx, dy, dz = vector
		previous = None
		for _ in xrange(max_distance * m):
			key = normalize((x, y, z))
			if key != previous and key in self.world:
				return key, previous
			previous = key
			x, y, z = x + dx / m, y + dy / m, z + dz / m
		return None, None

	def exposed(self, position):
		""" Returns False is given `position` is surrounded on all 6 sides by
		blocks, True otherwise.

		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			if ((x + dx, y + dy, z + dz) not in self.world) or (self.world[(x + dx, y + dy, z + dz)]==blocdisponibles["BUISSON"]) or (self.world[(x + dx, y + dy, z + dz)]==blocdisponibles["FLOWER"]): #mettre le non du bloc de petits blocs (voir en partie a travers)  
				return True
		return False

	def add_block(self, position, texture, immediate=True):
		global positionpremierbloc
		
		""" Add a block with the given `texture` and `position` to the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to add.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.
		immediate : bool
			Whether or not to draw the block immediately.

		"""
		if enregistrementdemodele == True:
			if modeleenenregistrement == {}:
				positionpremierbloc=position
			modeleenenregistrement[(position[0]-positionpremierbloc[0],position[1]-positionpremierbloc[1],position[2]-positionpremierbloc[2])]=texture
		modifsasauvegarder[position]=texture
		if position in self.world:
			self.remove_block(position, immediate)
		self.world[position] = texture
		self.sectors.setdefault(sectorize(position), []).append(position)
		if immediate:
			if self.exposed(position):
				self.show_block(position)
			self.check_neighbors(position)

	def remove_block(self, position, immediate=True):
		""" Remove the block at the given `position`.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to remove.
		immediate : bool
			Whether or not to immediately remove block from canvas.

		"""
		try:
			del modifsasauvegarder[position]
		except:
			modifsasauvegarder[position]="pasblocpasbloc"
		if position in self.world:
			del self.world[position]
			self.sectors[sectorize(position)].remove(position)
			if immediate:
				if position in self.shown:
					self.hide_block(position)
				self.check_neighbors(position)
		else:
			pass

	def check_neighbors(self, position):
		""" Check all blocks surrounding `position` and ensure their visual
		state is current. This means hiding blocks that are not exposed and
		ensuring that all exposed blocks are shown. Usually used after a block
		is added or removed.

		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key not in self.world:
				continue
			if self.exposed(key):
				if key not in self.shown:
					self.show_block(key)
			else:
				if key in self.shown:
					self.hide_block(key)

	def show_block(self, position, immediate=True):
		""" Show the block at the given `position`. This method assumes the
		block has already been added with add_block()

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		immediate : bool
			Whether or not to show the block immediately.

		"""
		texture = self.world[position]
		self.shown[position] = texture
		if immediate:
			self._show_block(position, texture)
		else:
			self._enqueue(self._show_block, position, texture)

	def _show_block(self, position, texture):
		""" Private implementation of the `show_block()` method.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.

		"""
		x, y, z = position
		if texture == blocdisponibles["BUISSON"] :
			vertex_data = cube_vertices(x, y+0.1, z, 0.4)
			texture_data = list(texture)
			# create vertex list
			# FIXME Maybe `add_indexed()` should be used instead
			self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
				('v3f/static', vertex_data),
				('t2f/static', texture_data))
			vertex_data = cube_vertices(x, y-0.4, z, 0.1)
			texture_data = list(blocdisponibles["TRONC"])
			# create vertex list
			# FIXME Maybe `add_indexed()` should be used instead
			self._shown[(x,y+100,z)] = self.batch.add(24, GL_QUADS, self.group,
				('v3f/static', vertex_data),
				('t2f/static', texture_data))
		elif texture == blocdisponibles["FLOWER"] :
			vertex_data = cube_vertices(x, y-0.1, z, 0.2)
			texture_data = list(texture)
			# create vertex list
			# FIXME Maybe `add_indexed()` should be used instead
			self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
				('v3f/static', vertex_data),
				('t2f/static', texture_data))
			vertex_data = cube_vertices(x, y-0.4, z, 0.1)
			texture_data = list(blocdisponibles["BUISSON"])
			# create vertex list
			# FIXME Maybe `add_indexed()` should be used instead
			self._shown[(x,y+100,z)] = self.batch.add(24, GL_QUADS, self.group,
				('v3f/static', vertex_data),
				('t2f/static', texture_data))
		else :
			vertex_data = cube_vertices(x, y, z, 0.5)
			texture_data = list(texture)
			# create vertex list
			# FIXME Maybe `add_indexed()` should be used instead
			self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
				('v3f/static', vertex_data),
				('t2f/static', texture_data))

	def hide_block(self, position, immediate=True):
		""" Hide the block at the given `position`. Hiding does not remove the
		block from the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to hide.
		immediate : bool
			Whether or not to immediately remove the block from the canvas.

		"""
		self.shown.pop(position)
		if immediate:
			self._hide_block(position)
		else:
			self._enqueue(self._hide_block, position)

	def _hide_block(self, position):
		""" Private implementation of the 'hide_block()` method.

		"""
		x, y, z = position
		#if self.world[position] == BUISSON or self.world[position] == FLOWER:
		try :
			self._shown.pop((x,y+100,z)).delete()
		except :
			pass
		# pose probleme si on ne fait pas les test pour les PNJ car ils rentrent et sortent de self.shown tout seuls
		try :
			self._shown.pop(position).delete()
		except :
			pass

	def show_sector(self, sector):
		""" Ensure all blocks in the given sector that should be shown are
		drawn to the canvas.

		"""
		for position in self.sectors.get(sector, []):
			if position not in self.shown and self.exposed(position):
				self.show_block(position, False)

	def hide_sector(self, sector):
		""" Ensure all blocks in the given sector that should be hidden are
		removed from the canvas.

		"""
		for position in self.sectors.get(sector, []):
			if position in self.shown:
				self.hide_block(position, False)

	def change_sectors(self, before, after):
		""" Move from sector `before` to sector `after`. A sector is a
		contiguous x, y sub-region of world. Sectors are used to speed up
		world rendering.

		"""
		before_set = set()
		after_set = set()
		pad = 4
		for dx in xrange(-pad, pad + 1):
			for dy in [0]:  # xrange(-pad, pad + 1):
				for dz in xrange(-pad, pad + 1):
					if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
						continue
					if before:
						x, y, z = before
						before_set.add((x + dx, y + dy, z + dz))
					if after:
						x, y, z = after
						after_set.add((x + dx, y + dy, z + dz))
		show = after_set - before_set
		hide = before_set - after_set
		for sector in show:
			self.show_sector(sector)
		for sector in hide:
			self.hide_sector(sector)

	def _enqueue(self, func, *args):
		""" Add `func` to the internal queue.

		"""
		self.queue.append((func, args))

	def _dequeue(self):
		""" Pop the top function from the internal queue and call it.

		"""
		func, args = self.queue.popleft()
		func(*args)

	def process_queue(self):
		""" Process the entire queue while taking periodic breaks. This allows
		the game loop to run smoothly. The queue contains calls to
		_show_block() and _hide_block() so this method should be called if
		add_block() or remove_block() was called with immediate=False

		"""
		start = time.clock()
		while self.queue and time.clock() - start < 1.0 / TICKS_PER_SEC:
			self._dequeue()

	def process_entire_queue(self):
		""" Process the entire queue with no breaks.

		"""
		while self.queue:
			self._dequeue()


class Window(pyglet.window.Window):


	global enregistrementdemodele

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)

		# Whether or not the window exclusively captures the mouse.
		self.exclusive = False

		# When flying gravity has no effect and speed is increased.
		self.flying = False

		# Creative mode (bloc illimite)
		self.creative = False

		# Strafing is moving lateral to the direction you are facing,
		# e.g. moving to the left or right while continuing to face forward.
		#
		# First element is -1 when moving forward, 1 when moving back, and 0
		# otherwise. The second element is -1 when moving left, 1 when moving
		# right, and 0 otherwise.
		self.strafe = [0, 0]

		# Current (x, y, z) position in the world, specified with floats. Note
		# that, perhaps unlike in math class, the y-axis is the vertical axis.
		if int(snoise3(0,0,graine, octaves,persistance) * 14.0 + 15.0) < 11:
			self.position = (0, 12, 0)
		else :
			self.position = (0, int(snoise3(0,0,graine, octaves,persistance) * 14.0 + 15.0)+2, 0)


		# First element is rotation of the player in the x-z plane (ground
		# plane) measured from the z-axis down. The second is the rotation
		# angle from the ground plane up. Rotation is in degrees.
		#
		# The vertical plane rotation ranges from -90 (looking straight down) to
		# 90 (looking straight up). The horizontal rotation range is unbounded.
		self.rotation = (0, 0)

		# Which sector the player is currently in.
		self.sector = None

		# The crosshairs at the center of the screen.
		self.reticle = None

		# Velocity in the y (upward) direction.
		self.dy = 0

		# A list of blocks the player can place. Hit num keys to cycle.
		# Il faudra pas mettre tous les blocs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		self.inventory = ["BRICK", "GRASS", "SAND", "WATER", "STONED", "BUISSON", "DIRT","FLOWER", "PNJTETE","PNJCORP","TRONC"]

		#Qtite de chaque bloc ds l'inventaire. Il faudra changer les nom de variables
		self.inventaire={}
		for elt in self.inventory:
			self.inventaire[elt]=0
		
		# a ameillorer pour le chargement et l'appartition
		batchinventaire = pyglet.graphics.Batch()
		sprites = []
		self.blocs = pyglet.image.load('Donnees/Images/textureYOGSCAST-OS.png')
		absisse = 100
		for elt in self.inventory:
			
			limage = self.blocs.get_region(x=32*0, y=32*0, width=32, height=32)
			lesprite = pyglet.sprite.Sprite(img=limage,x=100,y=absisse, batch = batchinventaire)
			sprites.append(lesprite)
			absisse = absisse + 50
		
#		self.dirt = self.blocs.get_region(x=32*0, y=32*0, width=32, height=32)
#		self.interfaceinventaire = pyglet.sprite.Sprite(img=self.dirt,x=100,y=100)
		

		# The current block the user can place. Hit num keys to cycle.
		self.block = self.inventory[0]

		# Convenience list of num keys.
		self.num_keys = [
			key._1, key._2, key._3, key._4, key._5,
			key._6, key._7, key._8, key._9, key._0]

		# Instance of the model that handles the world.
		"""
		if choix == 1:
			self.model = Model()
			picklableMethod = MethodProxy(self.model,self.model.world)
			cpickle.dump( pickableMethod, open( "Sauvegardes/saveWorld.p", "wb" ) )
		elif choix == 2:
			self.model = cpickle.load( open( "Sauvegardes/saveWorld.p", "rb" ) )
		"""
		self.model = Model()


		# The label that is displayed in the top left of the canvas.
		self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
			x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))

		# This call schedules the `update()` method to be called
		# TICKS_PER_SEC. This is the main game event loop.
		pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
		pyglet.clock.schedule_interval(self.appelerdeplacerPNJ, 1.0)



	def appelerdeplacerPNJ(self,deltat):
		xyz = self.get_sight_vector()
		x,y,z=self.position
		Model.deplacerPNJ(self.model,xyz,(x,y,z))
	
	
	"""
	def deplacerPNJ(self):
		for PNJ in dicoPNJ:
			if dicopositiondesPNJ[PNJ] == len(dicotrajectoirePNJ[PNJ]):
				pass
			else:
				temp=dicotrajectoirePNJ[PNJ]
				dicopositiondesPNJ[PNJ]=dicopositiondesPNJ[PNJ]+1
				pos=dicopositiondesPNJ[PNJ]
				Model.add_block(self.model,temp[pos], PNJCORP, immediate=False)
				Model.add_block(self.model,(temp[pos][0],temp[pos][1]+1,temp[pos][2]), PNJTETE, immediate=False)

	"""


	def set_exclusive_mouse(self, exclusive):
		""" If `exclusive` is True, the game will capture the mouse, if False
		the game will ignore the mouse.

		"""
		super(Window, self).set_exclusive_mouse(exclusive)
		self.exclusive = exclusive

	def get_sight_vector(self):
		""" Returns the current line of sight vector indicating the direction
		the player is looking.

		"""
		x, y = self.rotation
		# y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
		# is 1 when looking ahead parallel to the ground and 0 when looking
		# straight up or down.
		m = math.cos(math.radians(y))
		# dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
		# looking straight up.
		dy = math.sin(math.radians(y))
		dx = math.cos(math.radians(x - 90)) * m
		dz = math.sin(math.radians(x - 90)) * m
		return (dx, dy, dz)

	def get_motion_vector(self):
		""" Returns the current motion vector indicating the velocity of the
		player.

		Returns
		-------
		vector : tuple of len 3
			Tuple containing the velocity in x, y, and z respectively.

		"""
		if any(self.strafe):
			x, y = self.rotation
			strafe = math.degrees(math.atan2(*self.strafe))
			y_angle = math.radians(y)
			x_angle = math.radians(x + strafe)
			if self.flying:
				m = math.cos(y_angle)
				dy = math.sin(y_angle)
				if self.strafe[1]:
					# Moving left or right.
					dy = 0.0
					m = 1
				if self.strafe[0] > 0:
					# Moving backwards.
					dy *= -1
				# When you are flying up or down, you have less left and right
				# motion.
				dx = math.cos(x_angle) * m
				dz = math.sin(x_angle) * m
			else:
				dy = 0.0
				dx = math.cos(x_angle)
				dz = math.sin(x_angle)
		else:
			dy = 0.0
			dx = 0.0
			dz = 0.0
		return (dx, dy, dz)





	def update(self, dt):
		""" This method is scheduled to be called repeatedly by the pyglet
		clock.

		Parameters
		----------
		dt : float
			The change in time since the last call.

		"""
		self.model.process_queue()
		sector = sectorize(self.position)
		if sector != self.sector:
			self.model.change_sectors(self.sector, sector)
			if self.sector is None:
				self.model.process_entire_queue()
			self.sector = sector
		m = 8
		dt = min(dt, 0.2)
		for _ in xrange(m):
			self._update(dt / m)

	def _update(self, dt):
		""" Private implementation of the `update()` method. This is where most
		of the motion logic lives, along with gravity and collision detection.

		Parameters
		----------
		dt : float
			The change in time since the last call.

		"""
		# walking
		speed = FLYING_SPEED if self.flying else WALKING_SPEED
		d = dt * speed # distance covered this tick.
		dx, dy, dz = self.get_motion_vector()
		# New position in space, before accounting for gravity.
		dx, dy, dz = dx * d, dy * d, dz * d
		# gravity
		if not self.flying:
			# Update your vertical speed: if you are falling, speed up until you
			# hit terminal velocity; if you are jumping, slow down until you
			# start falling.
			self.dy -= dt * GRAVITY
			self.dy = max(self.dy, -TERMINAL_VELOCITY)
			dy += self.dy * dt
		# collisions
		x, y, z = self.position
		x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
		self.position = (x, y, z)

	def collide(self, position, height):
		""" Checks to see if the player at the given `position` and `height`
		is colliding with any blocks in the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check for collisions at.
		height : int or float
			The height of the player.

		Returns
		-------
		position : tuple of len 3
			The new position of the player taking into account collisions.

		"""
		# How much overlap with a dimension of a surrounding block you need to
		# have to count as a collision. If 0, touching terrain at all counts as
		# a collision. If .49, you sink into the ground, as if walking through
		# tall grass. If >= .5, you'll fall through the ground.
		pad = 0.25
		p = list(position)
		np = normalize(position)
		for face in FACES:  # check all surrounding blocks
			for i in xrange(3):  # check each dimension independently
				if not face[i]:
					continue
				# How much overlap you have with this dimension.
				d = (p[i] - np[i]) * face[i]
				if d < pad:
					continue
				for dy in xrange(height):  # check each height
					op = list(np)
					op[1] -= dy
					op[i] += face[i]
					if tuple(op) not in self.model.world or self.model.world[tuple(op)] == blocdisponibles["BUISSON"] or self.model.world[tuple(op)] == blocdisponibles["FLOWER"]: #Mettre le nom du bloc traversable par le joueur
						continue
					p[i] -= (d - pad) * face[i]
					if face == (0, -1, 0) or face == (0, 1, 0):
						# You are colliding with the ground or ceiling, so stop
						# falling / rising.
						self.dy = 0
					break
		return tuple(p)

	def on_mouse_press(self, x, y, button, modifiers):
		""" Called when a mouse button is pressed. See pyglet docs for button
		amd modifier mappings.

		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		button : int
			Number representing mouse button that was clicked. 1 = left button,
			4 = right button.
		modifiers : int
			Number representing any modifying keys that were pressed when the
			mouse button was clicked.

		"""
		if self.exclusive:
			vector = self.get_sight_vector()
			block, previous = self.model.hit_test(self.position, vector)
			if (button == mouse.RIGHT) or \
					((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
				# ON OSX, control + left click = right click.
				if previous:
					if self.creative:
						self.model.add_block(previous, blocdisponibles[self.block])
					else :
						if self.inventaire[self.block] != 0:
							self.model.add_block(previous, blocdisponibles[self.block])
							self.inventaire[self.block] = self.inventaire[self.block] - 1
			elif button == pyglet.window.mouse.LEFT and block:
				texture = self.model.world[block]
				if texture != blocdisponibles["STONE"]: # mettre ici les bloc indestructibles (ou faire un liste plus popre)
					for clee,elt in blocdisponibles.items():
						if elt == texture:
							tex = clee
					self.inventaire[tex] = self.inventaire[tex] + 1
					self.model.remove_block(block)
		else:
			self.set_exclusive_mouse(True)

	def on_mouse_motion(self, x, y, dx, dy):
		""" Called when the player moves the mouse.

		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		dx, dy : float
			The movement of the mouse.

		"""
		if self.exclusive:
			m = 0.15
			x, y = self.rotation
			x, y = x + dx * m, y + dy * m
			y = max(-90, min(90, y))
			self.rotation = (x, y)

	"""
	def save(self):
		pickle.dump( self.model.world, open( "Sauvegardes/saveWorld.p", "wb" ) )
		pickle.dump( self.model.shown, open( "Sauvegardes/saveShown.p", "wb" ) )
		pickle.dump( self.model._shown, open( "Sauvegardes/save_Shown.p", "wb" ) )
		pickle.dump( self.model.sectors, open( "Sauvegardes/saveSectors.p", "wb" ) )
		pickle.dump( self.model.biomes, open( "Sauvegardes/saveBiomes.p", "wb" ) )
		pickle.dump( self.model.interet, open( "Sauvegardes/saveInteret.p", "wb" ) )
	"""

	def on_key_press(self, symbol, modifiers):
		global modeleenenregistrement
		""" Called when the player presses a key. See pyglet docs for key
		mappings.

		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.

		"""
		global enregistrementdemodele
		if symbol == key.Z:
			self.strafe[0] -= 1
		elif symbol == key.S:
			self.strafe[0] += 1
		elif symbol == key.Q:
			self.strafe[1] -= 1
		elif symbol == key.D:
			self.strafe[1] += 1
		elif symbol == key.C:
			nomcapture='Sauvegardes/Captures/'+str(graine)+'-'+str(time.time())+'.png'
			pyglet.image.get_buffer_manager().get_color_buffer().save(nomcapture)
		elif symbol == key.W:
#			sauvegarde = 1
			self.model.save()
#			picklableMethod = MethodProxy(Model, Model.model)
#			cpickle.dump( picklableMethod, open( "Sauvegardes/saveWorld.p", "wb" ) )
		elif symbol == key.N:
			if enregistrementdemodele == False:
				enregistrementdemodele = True
			else :
				enregistrementdemodele = False
				positionpremierbloc=(0,0,0)
				pickle.dump( modeleenenregistrement, open( "Sauvegardes/MesModeles/modele.p", "wb" ) )
				modeleenenregistrement={}
		elif symbol == key.SPACE:
			if self.dy == 0:
				self.dy = JUMP_SPEED
		elif symbol == key.ESCAPE:
			self.set_exclusive_mouse(False)
		elif symbol == key.TAB:
			self.flying = not self.flying
		elif symbol == key.B:
			self.creative = not self.creative
		elif symbol in self.num_keys:
			index = (symbol - self.num_keys[0]) % len(self.inventory)
			self.block = self.inventory[index]

	def on_key_release(self, symbol, modifiers):
		""" Called when the player releases a key. See pyglet docs for key
		mappings.

		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.

		"""
		if symbol == key.Z:
			self.strafe[0] += 1
		elif symbol == key.S:
			self.strafe[0] -= 1
		elif symbol == key.Q:
			self.strafe[1] += 1
		elif symbol == key.D:
			self.strafe[1] -= 1

	def on_resize(self, width, height):
		""" Called when the window is resized to a new `width` and `height`.
		"""
		# label
		self.label.y = height - 10
		# reticle
		if self.reticle:
			self.reticle.delete()
		x, y = self.width / 2, self.height / 2
		n = 10
		self.reticle = pyglet.graphics.vertex_list(4,
			('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
		)

	def set_2d(self):
		""" Configure OpenGL to draw in 2d.

		"""
		width, height = self.get_size()
		glDisable(GL_DEPTH_TEST)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_3d(self):
		""" Configure OpenGL to draw in 3d.

		"""
		width, height = self.get_size()
		glEnable(GL_DEPTH_TEST)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65.0, width / float(height), 0.1, 60.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		x, y = self.rotation
		glRotatef(x, 0, 1, 0)
		glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
		x, y, z = self.position
		glTranslatef(-x, -y, -z)

	def on_draw(self):
		""" Called by pyglet to draw the canvas.

		"""
		self.clear()
		self.set_3d()
		glColor3d(1, 1, 1)
		self.model.batch.draw()
		self.draw_focused_block()
		self.set_2d()
		self.draw_label()
		self.draw_reticle()
		self.draw_inventaire()


	def draw_inventaire(self):
		pass
#		self.interfaceinventaire.draw()


	def draw_focused_block(self):
		""" Draw black edges around the block that is currently under the
		crosshairs.

		"""
		vector = self.get_sight_vector()
		block = self.model.hit_test(self.position, vector)[0]
		if block:
			x, y, z = block
			vertex_data = cube_vertices(x, y, z, 0.51)
			glColor3d(0, 0, 0)
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
			pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	def draw_label(self):
		""" Draw the label in the top left of the screen.

		"""
		global enregistrementdemodele
		if enregistrementdemodele == False :
			x, y, z = self.position
			self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
				pyglet.clock.get_fps(), x, y, z,
				len(self.model._shown), len(self.model.world))
			self.label.draw()
		else :
			x, y, z = self.position
			self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d rec' % (
				pyglet.clock.get_fps(), x, y, z,
				len(self.model._shown), len(self.model.world))
			self.label.draw()

	def draw_reticle(self):
		""" Draw the crosshairs in the center of the screen.

		"""
		glColor3d(0, 0, 0)
		self.reticle.draw(GL_LINES)


def setup_fog():
	""" Configure the OpenGL fog properties.

	"""
	# Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
	# post-texturing color."
	glEnable(GL_FOG)
	# Set the fog color.
	glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
	# Say we have no preference between rendering speed and quality.
	glHint(GL_FOG_HINT, GL_DONT_CARE)
	# Specify the equation used to compute the blending factor.
	glFogi(GL_FOG_MODE, GL_LINEAR)
	# How close and far away fog starts and ends. The closer the start and end,
	# the denser the fog in the fog range.
	glFogf(GL_FOG_START, 20.0)
	glFogf(GL_FOG_END, 60.0)


def setup():
	""" Basic OpenGL configuration.

	"""
	# Set the color of "clear", i.e. the sky, in rgba.
	glClearColor(0.5, 0.69, 1.0, 1)
	# Enable culling (not rendering) of back-facing facets -- facets that aren't
	# visible to you.
	glEnable(GL_CULL_FACE)
	# Set the texture minification/magnification function to GL_NEAREST (nearest
	# in Manhattan distance) to the specified texture coordinates. GL_NEAREST
	# "is generally faster than GL_LINEAR, but it can produce textured images
	# with sharper edges because the transition between texture elements is not
	# as smooth."
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	setup_fog()


def main():
	window = Window(width=800, height=600, caption='ODFv0.3', resizable=True)
	# Hide the mouse cursor and prevent the mouse from leaving the window.
	window.set_exclusive_mouse(False)
	setup()
	pyglet.app.run()


def initialisations():
	random.seed(graine)
	chargeblocs("Donnees/blocs.bloc")



class MethodProxy(object):
	def __init__(self, obj, method):
		self.obj = obj
		if isinstance(method, basestring):
			self.methodName = method
		else:
			assert callable(method)
			self.methodName = method.func_name

	def __call__(self, *args, **kwargs):
		return getattr(self.obj, self.methodName)(*args, **kwargs)

class Rect:
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
 
	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)
 
	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(room):
	global mapdungeon
	#go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			mapdungeon[x][y] = True
 
def create_h_tunnel(x1, x2, y):
	global mapdungeon
	#horizontal tunnel. min() and max() are used in case x1>x2
	for x in range(min(x1, x2), max(x1, x2) + 1):
		mapdungeon[x][y] = True
 
def create_v_tunnel(y1, y2, x):
	global mapdungeon
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		mapdungeon[x][y] = True
 
def make_map():
	global mapdungeon, player 
	global positiondebutdongeonx,positiondebutdongeony
	#fill map with "blocked" tiles
	 
	rooms = []
	num_rooms = 0
	
	for r in range(MAX_ROOMS):
		#random width and height
		w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = random.randint(1, MAP_WIDTH - w - 2)
		y = random.randint(1, MAP_HEIGHT - h - 2)
		
		#"Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)
		
		#run through the other rooms and see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
		
		if not failed:
			#this means there are no intersections, so this room is valid
			
			#"paint" it to the map's tiles
			create_room(new_room)
			
			#center coordinates of new room, will be useful later
			(new_x, new_y) = new_room.center()
			
			if num_rooms == 0:
				positiondebutdongeonx,positiondebutdongeony=new_x,new_y#this is the first room, where the player starts at
				pass
			else:
				#all rooms after the first:
				#connect it to the previous room with a tunnel
			
				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms-1].center()
			
				#draw a coin (random number that is either 0 or 1)
				if random.randint(0, 1) == 1:
					#first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					#first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
			
			#finally, append the new room to the list
			rooms.append(new_room)
			num_rooms += 1


#picklableMethod = MethodProxy(someObj, someObj.method)

if __name__ == '__main__':
	initialisations()
	choix = menu()
	while choix ==0:
		continue
	main()

