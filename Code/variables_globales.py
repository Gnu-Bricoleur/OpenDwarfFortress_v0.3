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

souriex,souriey = 0,0
afficherfenetrecraft = False

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

listeZombie = []
zombies_initialise = False

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

onpeutdiscuter = ["PNJTETE","PNJCORP","ZOMBIETETE","ZOMBIECORP"]

dicoBiome = {}
textdesquestions = ["[HAUT] Quel est ce village","[BAS] Sais-tu ou est le gouffre de Hraaa","[RIGHT] Au revoir"]
textdesreponses = ["C'est le village de Troupaumee bien sur, d'ou viens tu pour ne pas savoir ca ?","Je crois que le gouffre de Hraaa se situe plus a l'est","Salut","Qu'est ce que vous avez tous a me demander des quetes","Je ne suis pas sur d'avoir bien entendu"]
aafficher = []
blocdisponibles={}
blocscharge = {}
texturePNJ = {}
TEXTURE_PATH1 = 'Donnees/Images/textureYOGSCAST-OS.png'

TEXTURE_PATH2 = 'Donnees/Images/PNJ.png'
TEXTURE_PATH3 = 'Donnees/Images/outils.png'

pointdepassagevillageoismaison=[]
texteselec = -1
textetape = ""
flagTexteaetetape = False

tabfencraft = {}

FACES = [
	( 0, 1, 0),
	( 0,-1, 0),
	(-1, 0, 0),
	( 1, 0, 0),
	( 0, 0, 1),
	( 0, 0,-1),
]

pioche =  {(2,1):"TASBOIS", (2,2):"TASBOIS",(3,1):"TASCAILLASSE",(3,2):"TASCAILLASSE",(3,3):"TASCAILLASSE"}
hachette = {(2,1):"TASBOIS", (2,2):"TASBOIS",(3,1):"TASCAILLASSE",(3,2):"TASCAILLASSE",}
listecraftprdico = [pioche,hachette]
dicominicraft = {0:"PIOCHE",1:"HACHETTE"}

craftpossibles = []
craftexistants = [pioche,hachette]







# Variables pour physique !

blocseauforce = {}
arbres = {}
blocsaverifierpreau = []

blocsdeauajoute = []

dicoarbrestroncs = {}
dicoarbresfeuillages = {}
boiscoupe = []
arbreattaque = []

#Variables pour le multi !!!!!!!!!!

clientsconnecte = False

SERVEUR = False
CLIENT = False
adresseserveur = "localhost"
portserveur = "12800"

blocsaenvoyersup = []
blocsaenvoyerajo = []

blocsrecusup = []
blocsrecuajo = []

clients_connectes = []
clients_a_lire = []

connection_principale = None
connexion_avec_serveur = None
connexion_avec_client = None
