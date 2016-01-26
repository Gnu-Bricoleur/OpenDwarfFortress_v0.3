# OpenDwarfFortress_v0.3
Refonte du projet ODF avec pyglet (au lieu de pygame).  
L'objectif est de creer clone du jeu Dwarf Fortress en Open Source en améliorant l'interface et en ajoutant des fonctionnalitées tout en conservant la profondeur de jeu. Vous pouvez voir un exemple de monde generé dans le dossier Capture.  

Pour comprendre le code rendez vous sur le wiki : http://gnu-bricoleur.tuxfamily.org/dokuwiki/doku.php?id=start  

Et pour suivre l'avancement du projet, passez sur mon blog : http://gnu-bricoleur.tuxfamily.org/  
  
##Pour installer ODF, 4 petites étapes :   
Ouvrez une console dans le dossier ou vous souhaitez installer ODF et tapez :  
  
git clone https://github.com/Gnu-Bricoleur/OpenDwarfFortress_v0.3.git  
cd OpenDwarfFortress_v0.3  
pip install -r requirements.txt  
python main.py  

##Pour jouer :  
	-ZQSD pour se déplacer
	-TAB pour voler
	-clic droit pour poser un cube (selection dans l'inventaire avec le pavé numérique)
	-clic gauche pour detruire un cube
	-C pour prendre une capture 
	-W pour sauvegarder
	-N pour enregistrer un modèle


##Modifications :

###Le 2016/01/26 :
	-ajout de l'inventaire et premier pas vers une interface agreable.

###Le 2016/01/24 :
	-passage à la version 0.3 (voir TODO) et nettoyage du code. 

###Le 2016/01/21 :
	-ajout de "PNJ" suiveur de trajectoire en boucle mais problème dans la génération de trajectoire à partir de points d'interets

###Le 2016/01/20 :
	-ajout de points d'acces aux dongeons

###Le 2016/01/19 :
	-ajout de dongeons labirynthiques

###Le 2016/01/11 :
	-après en avoir bien bavé, ajout d'un systeme de sauvegarde

###Le 2015/12/19 :
	-implémentation des biomes
	-ajout des arbres (bug les gros arbres n'ont pas tjrs de feuilles)	

###Le 2015/12/17 :
	-apres 2 jours de galere avec la transparence, abandon et affichages de prtits blocs dans les gros blocs (BUISSON)
	- affichage des FLOXERa meme le sol (modification du tileset nessecaire pour l'image de fleur)

###Le 2015/12/15 :
	-ajout FLOWER et DIRT (pas d'herbe sous terre)
	-FLOWER en croisillon

###Le 2015/12/13 :
	-compatibilite avec texture minecraft
	-augmentation blocs ( eau et roc)
	-generation plus realiste
	-correction bug seed terrain plat
	-correction bug apparition dans un bloc

###Le 2015/12/12 :
	-empecher la capture de la souris pendant le chargement
	-fonctionnalitée de capture d'écran
	-generation du terrain avec noise
	-ajout d'une seed pour la generation
	-clavier AZERTY


## Crédits
OpenDwarfFortress est Open Source sous licences GPL (voir le fichier LICENCE)  
Si vous réutilisez mon code, je souhaite être crédité et si possible recevoir un message (ca fait plaisir d'avoir été utile).  

Les textures sont celles de YOGSCAST (Open Source). Le texture pack de base Minecraft est aussi présent dans le dossier Images, utile pour les tests, il n'est probablement pas sous licences libre mais étant disponible partout sur internet, je ne pense pas faire du tort à Mojang. Je n'en réclame pas crédit !   
La partie graphique du programme est basée sur le programme Open-Source de Michael Fogleman voir https://github.com/fogleman/Minecraft
