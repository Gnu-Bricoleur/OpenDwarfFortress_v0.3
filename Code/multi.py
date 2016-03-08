from variables_globales import *
from orphelins import *

import socket
import select

import math
import random
import time
import cPickle as pickle
from noise import *



def initreseau(cheminficconf):
	global portserveur, adresseserveur
	listelignes = []
	fichier = open(cheminficconf,'r')
	listelignesbrutes = fichier.readlines()
	for ligne in listelignesbrutes:
		if "#" in ligne:
			pass
		else:
#			l=ligne.split(",")
			listelignes.append(ligne)
	fichier.close()
	if len(listelignes) != 2:
		print "fichier de conf reseau invalide (nbr de ligne etrange ...)"
	else :
		# Si on veut charger d'autre choses depuis le fichier il faut l'ajouter la !!
		adresseserveur = str(listelignes[0])
		portserveur = int(listelignes[1])


def startserveur():
	global connexion_avec_client
	hote = ''
	port = 12800
	connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion_principale.bind((hote, port))
	connexion_principale.listen(5)
	print("Le serveur ecoute a present sur le port {}".format(port))
	connexion_avec_client, infos_connexion = connexion_principale.accept()
	grainep = pickle.dumps(graine)
	connexion_avec_client.send(grainep)
	"""
	serveur_lance = True
	clients_connectes = []
	connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)
	while not connexions_demandees :
		connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)
	for connexion in connexions_demandees:
		connexion_avec_client, infos_connexion = connexion.accept()
		# On ajoute le socket connecte a la liste des clients
		clients_connectes.append(connexion_avec_client)
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes,
				[], [], 0.05)
	except select.error:
		pass
	for client in clients_a_lire:
		client.send(graine)
		print "graine envoye"
	"""



def startclient():
	global connexion_avec_serveur
	hote = "localhost"
	port = 12800
	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion_avec_serveur.connect((hote, port))
	print("Connexion etablie avec le serveur sur le port {}".format(port))
	paquet = connexion_avec_serveur.recv(1024)
	while not paquet:
		paquet = connexion_avec_serveur.recv(1024)
		print paquet
	data = pickle.loads(paquet)
	return data

def stocksync(stckajo, stcksup):
	global blocsrecuajo,blocsrecusup
	if stckajo != []:
		blocsrecuajo.append(stckajo)
	if stcksup != []:
		blocsrecusup.append(stcksup)



def syncreseau(instancemodel):
	global clients_connectes,blocsrecuajo,blocsrecusup, clients_a_lire,connexion_avec_serveur, connexion_avec_client
	if blocsaenvoyerajo != [] or blocsaenvoyersup != []:
		if SERVEUR == True:
			while 1:
				paquet = client.recv(1024)
				if not paquet: break
				datarsup += paquet
			blocsrecusup = pickle.loads(datasup)
			while 1:
				paquet = client.recv(1024)
				if not paquet: break
				datarajo += paquet
			blocsrecuajo = pickle.loads(dataajo)
			datasup = pickle.dumps(blocsaenvoyersup)
			dataajo = pickle.dumps(blocsaenvoyerajo)
			client.send(datasup)
			time.sleep(0.05)
			client.send(dataajo)
		if CLIENT == True:
			datasup = pickle.dumps(blocsaenvoyersup)
			dataajo = pickle.dumps(blocsaenvoyerajo)
			connexion_avec_serveur.send(datasup)
			time.sleep(0.05)
			connexion_avec_serveur.send(dataajo)
			while 1:
				paquet = connexion_avec_serveur.recv(1024)
				if not paquet: break
				datarsup += paquet
			blocsrecusup = pickle.loads(datasup)
			while 1:
				paquet = connexion_avec_serveur.recv(1024)
				if not paquet: break
				datarajo += paquet
			blocsrecuajo = pickle.loads(dataajo)
		videliste(instancemodel)


def videliste(instancemodel):
	global blocsrecuajo,blocsrecusup
	print blocsrecuajo,blocsrecusup
	for bloc in blocsrecuajo:
		ext_add_block(instancemodel,bloc[0],bloc[1],True)
	for bloc in blocsrecusup:
#		print instancemodel.world[bloc]
		ext_remove_block(instancemodel,bloc,True)
	blocsrecuajo,blocsrecusup = [],[]




