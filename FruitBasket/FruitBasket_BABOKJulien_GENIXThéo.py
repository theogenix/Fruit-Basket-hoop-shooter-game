"""
FruitBasket_BABOKJulien_GENIXThéo

Créé le 15 avril 2020

Auteurs:
Théo Genix
Julien Babok

Dernière modification le 12 mai 2020
"""

import numpy as N
import scipy.integrate as SI
import matplotlib.pyplot as P
from math import *
import pygame
import time
import sys
import random
from pygame.locals import *

pygame.init()

#création musique
pygame.mixer.music.load('one piece.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)

#création bruitages
son_kobe_1=pygame.mixer.Sound('kobe1wav.wav')
son_cheering=pygame.mixer.Sound('cheering.wav')
son_buzzer=pygame.mixer.Sound('buzzer.wav')
pygame.mixer.Sound.set_volume(son_kobe_1,0.2)
pygame.mixer.Sound.set_volume(son_buzzer,0.1)
pygame.mixer.Sound.set_volume(son_cheering,0.2)

temps_init=time.time()

#valeurs des 4 positions pour les fruits
x1=700
x2=500
x3=300
x4=100

y=400

# Masse du fruit [kg]
mass=0.120

class Point:
    """Definition d'un point """
po=Point()
p0=Point()
p1=Point()
p2=Point()
p3=Point()
p4=Point()
p1.x=700
p1.y=400
p2.x=500
p2.y=400
p3.x=300
p3.y=400
p4.x=100
p4.y=400

position=1

pygame.display.set_caption("High score congrats!!")
ecran= pygame.display.set_mode((1000, 520))
         
#chargement et resize des images
arriere_plan= pygame.image.load('congrats.png')


def end_screen(the_score,ecran):
    '''Permet d'afficher l'image high score.
    Prend en entrée le score actuel et la fenêtre pour afficher l'image congrats'''
    running=True
    while running:
        ecran.blit(arriere_plan, (700,100))
        myfont3 = pygame.font.SysFont('Angry Birds', 60)
        Affichagehighscore = myfont3.render('Votre score est de '+ str(int(the_score)), True, white)
    
        pygame.display.flip()
        
       
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            
       
def lire():
    '''Permet de lire dans le fichier.txt et de retourner la valeur présente.
    Retourne le meilleur score précédente'''
    global high_score
    fichier=open("meilleur score.txt", "r")
    high_score=float(fichier.readline())
    fichier.close()
    return high_score
 
def write(the_score):
    '''Permet d'écrire dans le fichier.txt le nouveau meilleur score.
    Prends en entrée le score actuel'''
    fichier=open("meilleur score.txt", "w")
    fichier.write(str(the_score))
    fichier.close()
    
def calcul_vo(x,y):    
    '''le la vitesse vo du fruit suivant les coordonnées récupérées.
    Prend en entrée les coordonnées x,y du clic;
    Retourne la vitesse v0 du fruit selon ce clics'''
  
    v0 = sqrt((pow(x-p0.x,2) ) + (pow(y-p0.y,2)))/7

    return (v0)

def calcul_alt(x_clic,y_clic):
    '''Calcule l'angle alt entre vo et l'horizontale.
    Prend en entrée les coordonnées x,y du clic
    Retourne l'angle alt du fruit selon ce clic'''
    ab=x_clic-x
    cd=y_clic-y
    alt=N.arctan(-cd/ab)
    alt=degrees(alt)
    return alt

def fruits(level, position):
    '''Permet de définir une liste avec les masses des fruits à lancer en fonction du niveau et de la position du joueur.
    Prend donc en entrée le niveau et la position du joueur;
    Retourne une liste contenant les masses des fruits à lancer'''
    global fruits_a_lancer

    fruits_depart = [0.120, 0.01, 0.800, 0.015, 0.100]
    fruits_a_ajouter = [1.00, 0.160, 0.160]
    fruits_a_lancer = []

    for d in range(level + 2):
        fruits_a_lancer.append(fruits_depart[d])
    for j in range(position - 1):
        fruits_a_lancer.append(fruits_a_ajouter[j])

    return fruits_a_lancer


def calcul_trajectoire(v0, alt, mass):
    '''Calcule la trajectoire du fruit. Facilite le tir de certains fruits selon la position du joueur et la masse du fruit.
    Gère l'affichage du fruit durant la trajectoire selon la masse du fruit.
    Prend en entrée la vitesse initiale v0, l'angle alt et la masse du fruit.
    Retourne deux tableaux avec les coordonnées x et y du fruit durant sa trajectoire.'''
     
    g = 9.81      # Pesanteur [m/s2]
    cx = 0.45       # Coefficient de frottement d'une sphère
    rhoAir = 1.2    # Masse volumique de l'air [kg/m3] au niveau de la mer, T=20°C
    rad = 0.1748/2  # Rayon du boulet [m]
    rho = 6.23e3    # Masse volumique du boulet [kg/m3]

    if position==4:
        if 0.15>=mass>=0.02:
            alpha = 0.5*cx*rhoAir*N.pi*rad**2 / (2*mass) # Coefficient de frottement par unité de masse
        elif mass<0.02:
            alpha = 0.5*cx*rhoAir*N.pi*rad**2 / (2*(10*mass))
        else:
            alpha = 0.5*cx*rhoAir*N.pi*rad**2 / mass
    
    elif position==3 and mass==0.110:
        alpha = 0.5*cx*rhoAir*N.pi*rad**2 / (2*mass)
        
    else:
        if mass>=0.02:
            alpha = 0.5*cx*rhoAir*N.pi*rad**2 / (2*mass) # Coefficient de frottement par unité de masse
        elif mass<0.02:
            alpha = 0.5*cx*rhoAir*N.pi*rad**2 / (2*(10*mass))
        

    alt *= N.pi / 180.  # Inclinaison [rad]
    z0 = (0., 0., v0 * N.cos(alt), v0 * N.sin(alt)) # (x0, y0, vx0, vy0)
    tc = N.sqrt(mass / (g * alpha))
    t = N.linspace(0, tc, 100)
        
        
    def zdot(z, t):
        """Calcul de la dérivée de z=(x, y, vx, vy) à l'instant t."""
    
        x, y, vx, vy = z
        alphav = alpha * N.hypot(vx, vy)
        
        return (vx, vy, -alphav * vx, -g - alphav * vy) # dz/dt = (vx,vy,x..,y..)
        
    if mass>=0.5:
        zs = SI.odeint(zdot, z0, 3*t)
    elif 0.02<mass<0.5:
        zs = SI.odeint(zdot, z0, 10*t)
    elif mass<= 0.02:
        zs = SI.odeint(zdot, z0, 35*t)        
    ypos = zs[:,1]>=0 # y>0?

    
    #Coordonnées de X:
    X = zs[ypos,0].astype(int)
   
     
    #Coordonnées de Y:
    Y = zs[ypos,1].astype(int)

    
    return X, Y


#affichage fenêtre
pygame.display.set_caption("FruitBasket")
screen = pygame.display.set_mode((1000, 520))
         
#chargement et resize des images
background = pygame.image.load('Mur_Panier.png')


def load_image(w,level,position):
    '''Charge l'image du fruit à lancer.
    Prend en entré le niveau, la position, ainsi que la place du fruit dans le tableau des fruits.png.
    Retourne l'image chargée et redimensionnée, ainsi que le fruit correspondant.'''
    global liste_fruit_png
    global image_fruitpetit
    global fruits_marques
    liste_fruit_png=['citron.png','framboise.png','melon.png',"ananas.png",'banane.png',"pomme.png"]
    
    if level==2:
        liste_fruit_png.insert(3,'fraise.png')
        if position==1 and liste_fruit_png[w]=='citron.png':
            son_cheering.play() 
    
    if level==3:
        liste_fruit_png=['citron.png','framboise.png','melon.png',"fraise.png","kiwi.png","ananas.png",'banane.png',"pomme.png"]
        if position==1 and liste_fruit_png[w]=='citron.png':
            son_cheering.play() 
            
    try:
        fruits_marques=liste_fruit_png[w]
        image_fruit=pygame.image.load(str(liste_fruit_png[w]))
        image_fruitpetit=pygame.transform.scale(image_fruit,(60,60))
    except:
        running=False
        myfont2=pygame.font.SysFont('Halo',100)
        gameover=myfont2.render('Game Over',False,(50,198,86))
        screen.blit(gameover,(200,200))
        pygame.display.flip()
        high_score=lire()
        if the_score>high_score:
            write(the_score)        
            end_screen(the_score,ecran)
        pygame.quit()

    w+=1

    return()


def load_kobe(position):
    '''Place kobe sur des coordoonnées x et y suivant 4 positions différentes.
    Prend en entrée la position actuelle.
    Retourne les coordonnées correspondantes à la position.'''
    global image_kobepetit
    global x
    image_kobe=pygame.image.load("kobe_bogoss.png")
    image_kobepetit = pygame.transform.scale(image_kobe,(120,300))
    if position==1:
        p0.x=p1.x
        p0.y=p1.y
        x=x1
    if position==2:
        p0.x=p2.x
        p0.y=p2.y
        x=x2
    if position==3:
        p0.x=p3.x
        p0.y=p3.y
        x=x3
    if position==4:
        p0.x=p4.x
        p0.y=p4.y
        x=x4
    return(x,p0.x,p0.y)


        
load_kobe(position) 
white= (255,255,255)
level=1
w=0
the_score=0
load_image(w,level,position)
lire()


#boucle tant que pour condition running
running = True
o=1

Panier=False

last_space_press_time = 0

while running:
    #arrière plan appliqué
    screen.blit(background, (0,0))
    screen.blit(image_fruitpetit,(x,y))
    screen.blit(image_kobepetit,(p0.x-110,p0.y-90))
    
    myfont1=pygame.font.SysFont('Angry Birds',60)
    temps=myfont1.render(''+str(int(time.time()-temps_init)),False, (241,2,7))
    screen.blit(temps,(151,50))
    
    myfont2 = pygame.font.SysFont('Angry Birds', 40)
    Affichagescore = myfont2.render(''+ str(int(the_score)), True, white)
    screen.blit(Affichagescore,(100,147))
    
    myfont4 = pygame.font.SysFont('Angry Birds', 40)
    currenthg = myfont4.render(''+ str(int(high_score)), True, white)
    screen.blit(currenthg,(208,147))
    
    pygame.display.flip()

    for event in pygame.event.get():
        '''ferme le jeu si le joueur appuie sur croix'''
        if event.type == pygame.QUIT:
            running = False
            print("fermeture du jeu")

        # Trajectoire fruit    
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time - last_space_press_time >= 500:
                    last_space_press_time = current_time
                    try:
                        for i in range(len(X)):
                            xt = X[i]
                            yt = Y[i]
                            screen.blit(background, (0,0))
                            screen.blit(image_fruitpetit, (x+15*xt,y-15*yt))
                            screen.blit(image_kobepetit,(x-110,y-90))
                            pygame.display.flip()
                            if mass >= 1:
                                pygame.time.delay(30)
                            elif 0.5 <= mass < 1:
                                pygame.time.delay(20)
                            elif 0.02 < mass <= 0.5:
                                pygame.time.delay(10)
                            if Y[i-1] > Y[i]:
                                if 786 <= x+15*xt <= 896 and 190 <= y-15*yt <= 200:
                                    Panier = True
                                    kobe = random.choice([0, 1, 2])
                                    if kobe == 0: 
                                        pygame.mixer.music.pause()
                                        son_kobe_1.play()
                                        pygame.mixer.music.unpause()    
                    except:
                        continue         

        elif event.type == pygame.MOUSEBUTTONDOWN: #recupere coordonnées de x et y de la souris
            x_clic, y_clic = event.dict['pos']
            v0 = calcul_vo(x_clic, y_clic)
            alt = calcul_alt(x_clic, y_clic)
            X, Y = calcul_trajectoire(v0, alt, mass)
            Fruitslances = fruits(level, position)          
            if Panier: 
                if fruits_marques == 'citron.png':
                    the_score += 3
                if fruits_marques == 'framboise.png':
                    the_score += 4
                if fruits_marques == 'melon.png':
                    the_score += 9
                if fruits_marques == 'ananas.png':
                    the_score += 7
                if fruits_marques == 'banane.png':
                    the_score += 4
                if fruits_marques == 'pommme.png':
                    the_score += 5
                if fruits_marques == 'fraise.png':
                    the_score += 8
                if fruits_marques == 'kiwi.png':
                    the_score += 6

                Panier = False
                  
                o += 1
                massesfruits = fruits(level, position)
                w += 1
                              
                load_image(w, level, position)
                load_kobe(position)
                if position == 4 and level == 3 and liste_fruit_png[w] == 'pomme.png':
                    mass = massesfruits[o-1]
                    continue
                  
                if o == len(massesfruits):
                    position += 1
                    w = -1
                    o = 0
                    mass = massesfruits[o-1]
                      
                    if position == 5:
                        position = 1
                        level += 1
                else:
                    mass = massesfruits[o-1]
    
    t = 40
    if time.time()-temps_init > t:
        myfont2 = pygame.font.SysFont('Halo', 100)
        gameover = myfont2.render('Game Over', False, (50, 198, 86))
        screen.blit(gameover, (200, 200))
        pygame.display.flip()
        while time.time()-temps_init < t+1.4:
            pygame.mixer.music.stop()
            son_buzzer.play()
        
        high_score = lire()
        if the_score > high_score:
            write(the_score)
            end_screen(the_score, ecran)
        break
                
high_score = lire()
if the_score > high_score:
    write(the_score)        
    end_screen(the_score, ecran)

pygame.quit() 
 
                        