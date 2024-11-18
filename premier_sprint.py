# Nom du programme : premier sprint
# Auteur : Sofian
# Date : 11.11.2024
import pygame

# Initialisation de pygame
pygame.init()

# Fonction pour afficher le damier sans bordures
def afficher_damier():
    for i in range(nb_cases):
        x = i * largeur_rectangle
        couleur = (65, 42, 42) if i % 2 == 0 else (245, 245, 245)
        pygame.draw.rect(screen, couleur, (x, 0, largeur_rectangle, hauteur_rectangle))
    for i in range(nb_cases):
        x = i * largeur_rectangle
        couleur = (245, 245, 245) if i % 2 == 0 else (65, 42, 42)
        pygame.draw.rect(screen, couleur, (x, 100, largeur_rectangle, hauteur_rectangle))

# Fonction qui déplace le pion à droite
def bouge_droite():
    global positionx
    # Déplace le pion d'une case à droite
    positionx += 100
    # Empêcher le pion de dépasser la fin
    if positionx >= nb_cases * largeur_rectangle:
        positionx = 910
    screen.fill((255, 255, 255))
    afficher_damier()
    # Afficher le pion à sa position actuelle
    screen.blit(pion_img, (positionx, position_y))

# Fonction qui déplace le pion à gauche
def bouge_gauche():
    global positionx
    # Déplace le pion d'une case à gauche
    positionx -= 100
    # Empêcher le pion de dépasser la première case
    if positionx < 0:
        positionx = 10
    screen.fill((255, 255, 255))
    afficher_damier()
    # Afficher le pion à sa position actuelle
    screen.blit(pion_img, (positionx, position_y))

def bouge_haut():
    global position_y
    # Déplace le pion d'une case en haut
    position_y -= 100
    if position_y < 0:
        position_y = 10
    screen.fill((255, 255, 255))
    afficher_damier()
    # Afficher le pion à sa position actuelle
    screen.blit(pion_img, (positionx, position_y))

def bouge_bas():
    global position_y
    # Déplace le pion d'une case en haut
    position_y += 100
    if position_y > 100:
        position_y = 112
    screen.fill((255, 255, 255))
    afficher_damier()
    # Afficher le pion à sa position actuelle
    screen.blit(pion_img, (positionx, position_y))

# Variables
largeur_rectangle = 100
hauteur_rectangle = 100
nb_cases = 10
positionx = 10
position_y = 10
taille_case = 100
y = 100

# Fenêtre
screen = pygame.display.set_mode((1000, 200))

# Charger l'image du pion
pion_img = pygame.image.load("img\\MA-24_pion.png")
pion_img = pygame.transform.scale(pion_img, (80, 80))

afficher_damier()
# Afficher le pion à sa position actuelle
screen.blit(pion_img, (positionx, position_y))


# Boucle pour maintenir la fenêtre
running = True
while running:
    # Récupérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Déplacement du pion en fonction de la touche pressée
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

#essaie d'envoyer

