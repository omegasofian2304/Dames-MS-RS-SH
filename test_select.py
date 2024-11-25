import pygame

# Initialisation de pygame
pygame.init()

# Variables pour le damier
largeur_case = 70
hauteur_case = 70
nb_cases = 10

# Fenêtre
screen = pygame.display.set_mode((700, 700))

# Fonction pour afficher le damier
def afficher_damier():
    for ligne in range(nb_cases):
        for colonne in range(nb_cases):
            x = colonne * largeur_case
            y = ligne * hauteur_case
            couleur = (65, 42, 42) if (ligne + colonne) % 2 == 0 else (245, 245, 245)
            pygame.draw.rect(screen, couleur, (x, y, largeur_case, hauteur_case))

# Variables initiales pour le pion
positionx = 0
position_y = 630

# Charger l'image du pion
pion_img = pygame.image.load("img\\MA-24_pion.png")
pion_img = pygame.transform.scale(pion_img, (60, 60))

# Calculer l'offset pour centrer le pion dans la case
offset_x = (largeur_case - pion_img.get_width()) // 2
offset_y = (hauteur_case - pion_img.get_height()) // 2

# Variable pour l'aura
aura_active = False
couleur_contour = (255, 255, 0)
rayon_contour = (pion_img.get_width() // 2) + 5

# Fonction pour dessiner le contour jaune autour du pion
def dessiner_aura():
    if aura_active:
        # Calculer le centre du pion
        centre_x = positionx + largeur_case // 2
        centre_y = position_y + hauteur_case // 2
        # Dessiner un contour autour du pion, avec un rayon qui est exactement à la taille du pion
        pygame.draw.circle(screen, couleur_contour, (centre_x, centre_y), 30, 5)  # Aura de rayon 30 (collé au bord du pion)

# Afficher le damier et le pion à sa position initiale
afficher_damier()
screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))

# Boucle principale du programme
running = True
pion_selectionne = False  # Le pion n'est pas sélectionné au départ
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Cliquer sur le pion pour le sélectionner
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Obtenir la position de la souris
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Vérifier si le clic est sur le pion
            if positionx <= mouse_x <= positionx + largeur_case and position_y <= mouse_y <= position_y + hauteur_case:
                pion_selectionne = True
                aura_active = True  # L'aura s'affiche une fois que le pion est sélectionné

        # Déplacer le pion une fois sélectionné
        if event.type == pygame.MOUSEBUTTONDOWN and pion_selectionne:
            # Obtenir la position de la souris
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculer la case cible
            cible_x = (mouse_x // largeur_case) * largeur_case
            cible_y = (mouse_y // hauteur_case) * hauteur_case

            # Vérifier si le mouvement est une diagonale valide
            if (cible_x == positionx + largeur_case and cible_y == position_y - hauteur_case) or \
                    (cible_x == positionx - largeur_case and cible_y == position_y - hauteur_case) or \
                    (cible_x == positionx + largeur_case and cible_y == position_y + hauteur_case) or \
                    (cible_x == positionx - largeur_case and cible_y == position_y + hauteur_case):
                # Déplacer le pion
                positionx = cible_x
                position_y = cible_y

                # Désélectionner le pion et enlever l'aura après le mouvement
                pion_selectionne = False
                aura_active = False  # L'aura disparaît après le mouvement

            # Afficher le damier et le pion à la nouvelle position
            screen.fill((255, 255, 255))  # Effacer l'écran
            afficher_damier()  # Afficher le damier
            screen.blit(pion_img, (positionx + offset_x, position_y + offset_y))  # Afficher le pion
            dessiner_aura()  # Dessiner l'aura autour du pion si sélectionné

    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter pygame
pygame.quit()
