from variables_globales import *

import math
import random
import time
import cPickle as pickle
from noise import *






def ext_remove_block(model,position,immedia):
	model.remove_block(position,immedia)

def ext_add_block(model,position,block,immedia):
	model.add_block(position,block,immedia)



def testextaddblock(model):
	for z in range(0,100):
		ext_add_block(model,(0,z,0),blocdisponibles["SAND"],False)


def fenetredecraft(souriex,souriey,block,qte):
	global afficherfenetrecraft
	global tabfencraft
	craftchoisi = None
	anglex, angley = 150,150
	fin = False
	if (0<souriex<50) and (0<souriey<30 ) :
		afficherfenetrecraft = False
		fin = True
	if souriex !=0 and souriey !=0:
		for x in range(anglex,anglex+400,100):
			for y in range(angley, angley+400, 100):
				if x<souriex<x+100 and y<souriey<y+100 :
					if qte!=0 and block != None:
						tabfencraft[(((x-anglex)/100),((y-angley)/100))] = block
#						print tabfencraft
		if 500<souriex<532:
			for y in range(0,250,50):
				if y<souriey<y+50:
					craftchoisi = craftpossibles[(y/50)]
		souriex,soouriey = 0,0
	craftposs = evalcraft()
	return fin, craftposs, craftchoisi
#	return afficherfenetrecraft



def suffisamentdematos(craftchoisi, inventaire):
	for elt in craftchoisi:
		if inventaire[craftchoisi[elt]] -1 < 0:
			return False
	return True



def evalcraft():
	global craftpossibles
	global tabfencraft
	completude = 1
	craftpossibles = []
	for craft in craftexistants:
		for elt in craft:
			if elt in tabfencraft:
				if tabfencraft[elt] == craft[elt]:
					completude = completude +1
		if completude == len(craft.keys()):
			craftpossibles.append(craft)
	return craftpossibles




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
	for ligne in listelignes:                    # Si on veut charger d'autre choses depuis le fichier il faut l'ajouter la !!
		blocscharge[ligne[0]]=(int(ligne[1]),int(ligne[2]),int(ligne[3]),int(ligne[4]),int(ligne[5]),int(ligne[6]),int(ligne[7]),int(ligne[8]),int(ligne[9]))
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
	if x2-x1 != 0:
		a=(y2-y1)/(x2-x1)
		b=y1-(a*x1)
	else :
		a = 10000
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
#	print trajectoire
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
	return positiondebutdongeonx,positiondebutdongeony,
