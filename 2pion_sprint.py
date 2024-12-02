# Nom du programme : deuxieme sprint
# Auteur : sofia
# Date : 18.11.2024
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
position_y = 630  # Le pion commence en bas du damier (case (0, 9))
pos_2_x = 0
pos_2_y = 0
# Charger l'image du pion
pion_img = pygame.image.load("img\\MA-24_pion.png")
pion_img = pygame.transform.scale(pion_img, (60, 60)) # Taille du pion




# Fonction pour colorier l'image du pion
def colorier_image(image, couleur):
    # Créer une surface de la même taille que l'image
    overlay = pygame.Surface(image.get_size())
    overlay.fill(couleur)

    # Appliquer l'overlay (l'effet couleur)
    image_coloree = image.copy()
    image_coloree.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # L'effet de mélange

    return image_coloree



# Exemple d'utilisation dans le jeu
rouge = (255, 0, 0)  # Couleur rouge
bleu = (100, 100, 255) #couleur bleu
pion_img_coloree_r = colorier_image(pion_img, rouge)
pion_img_coloree_b = colorier_image(pion_img, bleu)

# Ensuite, vous pouvez afficher cette image colorée à la place de l'originale


# Calculer l'offset pour centrer le pion dans la case
offset_x = (largeur_case - pion_img.get_width()) // 2
offset_y = (hauteur_case - pion_img.get_height()) // 2

# Afficher le damier et le pion à sa position initiale
afficher_damier()
screen.blit(pion_img_coloree_b, (pos_2_x + offset_x, pos_2_y + offset_y))
screen.blit(pion_img_coloree_r, (positionx + offset_x, position_y + offset_y))
# Boucle principale du programme
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Déplacer le pion avec la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Obtenir la position de la souris
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculer la case cible
            cible_x = (mouse_x // largeur_case) * largeur_case
            cible_y = (mouse_y // hauteur_case) * hauteur_case

            # Vérifier si le mouvement est une diagonale vers l'avant
            if cible_x == positionx + largeur_case and cible_y == position_y - hauteur_case:
                positionx = cible_x
                position_y = cible_y
            if cible_x == positionx - largeur_case and cible_y == position_y - hauteur_case:
                positionx = cible_x
                position_y = cible_y

            if cible_x == positionx + largeur_case and cible_y == position_y + hauteur_case:
                positionx = cible_x
                position_y = cible_y
            if cible_x == positionx - largeur_case and cible_y == position_y + hauteur_case:
                positionx = cible_x
                position_y = cible_y

            # Afficher le damier et le pion à la nouvelle position
            screen.fill((255, 255, 255))  # Effacer l'écran
            afficher_damier()  # Afficher le damier
            screen.blit(pion_img_coloree_b, (pos_2_x + offset_x, pos_2_y + offset_y))
            screen.blit(pion_img_coloree_r, (positionx + offset_x, position_y + offset_y))# Afficher les pions

    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter pygame
pygame.quit()
