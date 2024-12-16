# Nom du programme : dame.py
# Auteur : sofian
# Date : 16.12.2024
import pygame

# Initialisation de pygame
pygame.init()

# Variables pour le damier
largeur_case = 70
hauteur_case = 70
nb_cases = 10
nb_ligne = 1
nb_case = 1

# Fenêtre
screen = pygame.display.set_mode((700, 700))

# Fonction pour afficher le damier
def afficher_damier():
    global nb_case, nb_ligne
    for h in range(nb_cases):  # Ligne
        for i in range(nb_cases):  # Colonnes
            x = i * largeur_case
            y = h * hauteur_case
            couleur = (65, 42, 42) if nb_case % 2 == 0 else (245, 245, 245)
            pygame.draw.rect(screen, couleur, (x, y, largeur_case, hauteur_case))
            nb_case += 1
        nb_case = nb_case + 1
    nb_ligne += 1

# Fonction pour déplacer le pion à droite
def bouge_droite():
    global positionx
    positionx += largeur_case
    # Empêcher de sortir à droite
    if positionx >= (nb_cases - 1) * largeur_case:
        positionx = (nb_cases - 1) * largeur_case
    afficher_damier()
    screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Fonction pour déplacer le pion à gauche
def bouge_gauche():
    global positionx
    positionx -= largeur_case
    # Empêcher de sortir à gauche
    if positionx < 0:
        positionx = 0
    afficher_damier()
    screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Fonction pour déplacer le pion vers le haut
def bouge_haut():
    global position_y
    position_y -= hauteur_case
    # Empêcher de sortir en haut
    if position_y < 0:
        position_y = 0
    afficher_damier()
    screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Fonction pour déplacer le pion vers le bas
def bouge_bas():
    global position_y
    position_y += hauteur_case
    # Empêcher de sortir en bas
    if position_y >= (nb_cases - 1) * hauteur_case:
        position_y = (nb_cases - 1) * hauteur_case
    afficher_damier()
    screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Variables initiales
positionx = 0
position_y = 0

# Charger l'image du pion
pion_img = pygame.image.load("img\\MA-24_pion.png")
pion_img = pygame.transform.scale(pion_img, (60, 60))  # Taille du pion

# Calculer l'offset pour centrer le pion dans la case
offset_x = (largeur_case - pion_img.get_width()) // 2
offset_y = (hauteur_case - pion_img.get_height()) // 2

# Afficher le damier et le pion à sa position initiale
afficher_damier()
screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Boucle principale du programme
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Déplacer le pion en fonction de la touche pressée
            if event.key == pygame.K_RIGHT:
                bouge_droite()
            elif event.key == pygame.K_LEFT:
                bouge_gauche()
            elif event.key == pygame.K_UP:
                bouge_haut()
            elif event.key == pygame.K_DOWN:
                bouge_bas()
            elif event.key == pygame.K_q:
                running = False

    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter pygame
pygame.quit()
