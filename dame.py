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

# Classe pour représenter un pion
class Pion:
    def __init__(self, x, y, couleur):
        self.x = x  # Position en x (coordonnée de la case)
        self.y = y  # Position en y (coordonnée de la case)
        self.couleur = couleur  # Couleur du pion ('blanc' ou 'noir')
        self.selected = False  # État de sélection du pion
        self.image = pygame.image.load("img\\MA-24_pion.png")  # Charger l'image du pion
        self.image = pygame.transform.scale(self.image, (60, 60))  # Redimensionner l'image
        self.offset_x = (largeur_case - self.image.get_width()) // 2  # Calculer l'offset horizontal
        self.offset_y = (hauteur_case - self.image.get_height()) // 2  # Calculer l'offset vertical

    # Afficher le pion à sa position actuelle
    def afficher(self):
        screen.blit(self.image, (self.x + self.offset_x, self.y + self.offset_y))

    # Sélectionner le pion
    def select(self):
        self.selected = True

    # Désélectionner le pion
    def deselect(self):
        self.selected = False

    # Déplacer le pion vers une nouvelle position
    def deplacer(self, nouvelle_x, nouvelle_y):
        self.x = nouvelle_x
        self.y = nouvelle_y

    # Vérifier si un clic est sur ce pion
    def check_selection(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + largeur_case and self.y <= mouse_y <= self.y + hauteur_case

# Créer la liste de pions
pions = []

# Disposition des pions blancs (sur les 4 premières lignes)
for i in range(4):
    for j in range(nb_cases):
        if (i + j) % 2 == 1:  # Seulement sur les cases noires
            pions.append(Pion(j * largeur_case, i * hauteur_case, 'blanc'))

# Disposition des pions noirs (sur les 4 dernières lignes)
for i in range(6, 10):
    for j in range(nb_cases):
        if (i + j) % 2 == 1:  # Seulement sur les cases noires
            pions.append(Pion(j * largeur_case, i * hauteur_case, 'noir'))

# Fonction pour afficher tous les pions
def afficher_pions():
    for pion in pions:
        pion.afficher()

# Boucle principale du programme
running = True
pion_selectionne = None  # Pion actuellement sélectionné
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Cliquer pour sélectionner un pion
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Si un pion est déjà sélectionné, essayer de le déplacer
            if pion_selectionne is not None:
                # Calculer la case cible
                cible_x = (mouse_x // largeur_case) * largeur_case
                cible_y = (mouse_y // hauteur_case) * hauteur_case

                # Vérifier si le mouvement est une diagonale valide pour les dames classiques
                if abs(cible_x - pion_selectionne.x) == largeur_case and abs(cible_y - pion_selectionne.y) == hauteur_case:
                    pion_selectionne.deplacer(cible_x, cible_y)  # Déplacer le pion

                # Désélectionner le pion après le déplacement
                pion_selectionne.deselect()
                pion_selectionne = None  # Réinitialiser la sélection
            else:
                # Si aucun pion n'est sélectionné, vérifier si on clique sur un pion
                for pion in pions:
                    if pion.check_selection(mouse_x, mouse_y):
                        pion.select()  # Sélectionner le pion
                        pion_selectionne = pion
                        break

        # Effacer l'écran et redessiner tout
        screen.fill((255, 255, 255))  # Effacer l'écran
        afficher_damier()  # Afficher le damier
        afficher_pions()  # Afficher les pions

    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter pygame
pygame.quit()