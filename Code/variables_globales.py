import math
import random
import time

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

UNDEMILARGEURLONGUEURDUMONDE = 80

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

# Mes variables globales 
octaves=5
tps=time.time()/1000.0
graine = (tps-int(tps))*1000.0
persistance=0.25
choix = 0
#global sauvegarde
sauvegarde = 0
modifsasauvegarder = {}
enregistrementdemodele = False
positionpremierbloc=(0,0,0)
modeleenenregistrement = {}
positiondebutdongeonx,positiondebutdongeony=0,0
dicoPNJ={}
dicotrajectoirePNJ={}
dicopositiondesPNJ={}
#a mettre dans un fichier et automatiser le chargement
"""
dicoPNJ["premierpnj"]=((5,10),(10,5),(-5,-5))
dicoPNJ["deuxiempnj"]=((3,-5),(4,15),(2,2))
"""

#size of the map du dungeon
MAP_WIDTH = 80
MAP_HEIGHT = 45
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
mapdungeon = [[ False
			for y in range(MAP_HEIGHT) ]
				for x in range(MAP_WIDTH) ]




TEXTURE_PATH = 'Donnees/Images/textureYOGSCAST-OS.png'







FACES = [
	( 0, 1, 0),
	( 0,-1, 0),
	(-1, 0, 0),
	( 1, 0, 0),
	( 0, 0, 1),
	( 0, 0,-1),
]



