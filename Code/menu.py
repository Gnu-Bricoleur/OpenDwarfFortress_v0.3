

import pygame
from pygame.locals import *


def menu():
	continuer = 1
	pygame.init()
	if not pygame.font: print('Warning, fonts disabled')
	if not pygame.mixer: print('Warning, sound disabled')


	pygame.display.set_caption("ODF v0.3")
	fenetre = pygame.display.set_mode((800,600))
	fenetre.fill((255, 255, 255))

	fond = pygame.image.load("Donnees/Images/fond.png").convert()

	fenetre.blit(fond, (0,0))
	
	print("### MENU ###")
	if pygame.font:
		font = pygame.font.Font("Donnees/SDS.ttf", 36)
		text = font.render("Open Dwarf Fortress v0.3", 1, (10, 10, 10))
		textpos = (100,50)
		fenetre.blit(text, textpos)
		
		font = pygame.font.Font("Donnees/SDS.ttf", 18)
		texta = font.render("(a)-Nouvelle partie", 1, (10, 10, 10))
		textz = font.render("(z)-Charger ancienne partie", 1, (10, 10, 10))
		texte = font.render("(e)-Quitter", 1, (10, 10, 10))
		textr = font.render("(r)-Tests", 1, (10, 10, 10))
		textposa = (200,200)
		textposz = (200,220)
		textpose = (200,240)
		textposr = (200,260)
		fenetre.blit(texta, textposa)
		fenetre.blit(textz, textposz)
		fenetre.blit(texte, textpose)
		fenetre.blit(textr, textposr)
		
		font = pygame.font.Font("Donnees/SDS.ttf", 8)
		text = font.render("credits : Sylvain Migaud", 1, (10, 10, 10))
		textpos = (50,400)
		fenetre.blit(text, textpos)
		pygame.display.flip()
	
	font = pygame.font.Font("Donnees/SDS.ttf", 18)
	
	while continuer:
		for event in pygame.event.get():   
			if event.type == QUIT:     
				continuer = 0  
			if event.type == KEYDOWN:
				if event.key == K_e:
					texte = font.render("(e)-Quitter", 1, (255, 10, 10))
					textpose = (200,240)
					fenetre.blit(texte, textpose)
					selection=0
				if event.key == K_a:
					texta = font.render("(a)-Nouvelle partie", 1, (10, 255, 10))
					textposa = (200,200)
					fenetre.blit(texta, textposa)
					choix=1
				if event.key == K_z:
					textz = font.render("(z)-Charger ancienne partie", 1, (10, 10, 255))
					textposz = (200,220)
					fenetre.blit(textz, textposz)
					choix=2
				if event.key == K_r:
					textz = font.render("(r)-Tests", 1, (255, 10, 255))
					textposz = (200,260)
					fenetre.blit(textz, textposz)
					choix=3
				if event.key == K_n:
					Model.save()
				if event.key == K_RETURN and choix != 0:
#					continuer=0
					return choix
				pygame.display.flip()
