# Nom du programme : sprint 40 pions
# Auteur : sofian
# Date : 02.12.2024
from tkinter.messagebox import showinfo
import time
import pygame
import sys

# Initialiser pygame
pygame.init()

# Définir les couleurs
BLANC = (255, 255, 255)
BRUN_BOIS_TERNE = (139, 69, 19)
NOIR = (0, 0, 0)
VERT = (0, 120, 0)
BLEU = (30, 30, 255)
ROUGE = (255, 0, 0)
GRIS_CLAIR = (200, 200, 200)

# Dimensions du plateau
taille_case = 75
taille_pion = 50
epaisseur_bordure = 15

# Passer en plein écran
LARGEUR_FENETRE, HAUTEUR_ECRAN = pygame.display.Info().current_w, pygame.display.Info().current_h
ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_ECRAN))
pygame.display.set_caption("Plateau de dames 10x10")

# Calculer les marges pour centrer le plateau
debut_x = (LARGEUR_FENETRE - 10 * taille_case - 2 * epaisseur_bordure) // 2
debut_y = (HAUTEUR_ECRAN - 10 * taille_case - 2 * epaisseur_bordure) // 2

# Charger et redimensionner les images des pions
image_pion = pygame.image.load("img\\MA-24_pion.png")
image_pion = pygame.transform.scale(image_pion, (taille_pion, taille_pion))

# variables pour stats
compteur_bleu = 0
compteur_rouge = 0


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
pion_rouge = colorier_image(image_pion, rouge)
pion_bleu = colorier_image(image_pion, bleu)

# Classe Pion
class Pion:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.selectionne = False
        self.est_reine = False

    def dessiner(self, ecran):
        if self.couleur == ROUGE:
            ecran.blit(pion_rouge, (self.x - taille_pion // 2, self.y - taille_pion // 2))
        elif self.couleur == BLEU:
            ecran.blit(pion_bleu, (self.x - taille_pion // 2, self.y - taille_pion // 2))
        if self.selectionne:
            pygame.draw.circle(ecran, (0, 255, 0), (self.x, self.y), taille_pion // 2 + 5, 3)
        if self.est_reine:
            pygame.draw.circle(ecran, GRIS_CLAIR, (self.x, self.y), taille_pion // 4)

    def contient_point(self, pos):
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= taille_pion // 2

    def deplacer(self, nouvelle_case):
        i, j = nouvelle_case
        self.x = debut_x + epaisseur_bordure + i * taille_case + taille_case // 2
        self.y = debut_y + epaisseur_bordure + j * taille_case + taille_case // 2

    def promouvoir_en_reine(self):
        self.est_reine = True

pions = []
# Initialiser les pions
def initialiser_pion():
    for i in range(10):
        for j in range(4):
            if (i + j) % 2 == 1:
                x = debut_x + epaisseur_bordure + i * taille_case + taille_case // 2
                y = debut_y + epaisseur_bordure + j * taille_case + taille_case // 2
                pions.append(Pion(x, y, ROUGE))

    for i in range(10):
        for j in range(6, 10):
            if (i + j) % 2 == 1:
                x = debut_x + epaisseur_bordure + i * taille_case + taille_case // 2
                y = debut_y + epaisseur_bordure + j * taille_case + taille_case // 2
                pions.append(Pion(x, y, BLEU))


initialiser_pion()

# Fonction pour dessiner l'échiquier
def dessiner_echiquier():
    ecran.fill(VERT)
    pygame.draw.rect(ecran, BRUN_BOIS_TERNE,
                     (debut_x, debut_y, 10 * taille_case + 2 * epaisseur_bordure, 10 * taille_case + 2
                      * epaisseur_bordure))

    for i in range(10):
        for j in range(10):
            x = debut_x + i * taille_case + epaisseur_bordure
            y = debut_y + j * taille_case + epaisseur_bordure
            if (i + j) % 2 == 1:
                pygame.draw.rect(ecran, NOIR, (x, y, taille_case, taille_case))
            else:
                pygame.draw.rect(ecran, BLANC, (x, y, taille_case, taille_case))

# Déterminer la case cliquée
def case_cliquee(pos):
    x, y = pos
    if debut_x + epaisseur_bordure <= x < debut_x + epaisseur_bordure + 10 * taille_case and \
            debut_y + epaisseur_bordure <= y < debut_y + epaisseur_bordure + 10 * taille_case:
        i = (x - debut_x - epaisseur_bordure) // taille_case
        j = (y - debut_y - epaisseur_bordure) // taille_case
        return int(i), int(j)
    return None

# Vérifier si la case d'arrivée est occupée par un autre pion
def case_occupee(case_arrivee):
    i, j = case_arrivee
    for pion in pions:
        if pion.x == debut_x + epaisseur_bordure + i * taille_case + taille_case // 2 and \
                pion.y == debut_y + epaisseur_bordure + j * taille_case + taille_case // 2:
            return pion
    return None

def mouvement_valide(case_depart, case_arrivee, pion_selectionne):
    capture_effectuee = False  # Variable pour suivre si une capture a eu lieu

    if not case_arrivee:
        return False, capture_effectuee

    i1, j1 = case_depart
    i2, j2 = case_arrivee

    # Vérifier si c'est une case noire
    if (i2 + j2) % 2 == 0:
        return False, capture_effectuee

    # Vérifier si la case d'arrivée est déjà occupée par un autre pion
    pion_occupe = case_occupee(case_arrivee)
    if pion_occupe:
        return False, capture_effectuee  # La case est occupée

    # Déplacement spécifique pour les reines
    if pion_selectionne.est_reine:
        # Logique de capture pour les reines (en diagonale)
        if abs(i2 - i1) != abs(j2 - j1):
            return False, capture_effectuee

        direction_i = 1 if i2 > i1 else -1
        direction_j = 1 if j2 > j1 else -1
        pions_rencontres = []

        for step in range(1, abs(i2 - i1)):
            interm_i = i1 + step * direction_i
            interm_j = j1 + step * direction_j
            pion_intermediaire = case_occupee((interm_i, interm_j))
            if pion_intermediaire:
                if pion_intermediaire.couleur == pion_selectionne.couleur:
                    return False, capture_effectuee  # Pion allié sur le chemin
                pions_rencontres.append(pion_intermediaire)

        if len(pions_rencontres) == 1:  # Capture valide
            pions.remove(pions_rencontres[0])  # Enlever le pion capturé
            capture_effectuee = True
            return True, capture_effectuee

        return True, capture_effectuee

    # Déplacement normal (non-reine) : mouvement de saut (2 cases)
    if abs(i2 - i1) == 2 and abs(j2 - j1) == 2:
        i_milieu = (i1 + i2) // 2
        j_milieu = (j1 + j2) // 2
        pion_sauter = case_occupee((i_milieu, j_milieu))
        if pion_sauter and pion_sauter.couleur != pion_selectionne.couleur:
            pions.remove(pion_sauter)  # Enlever le pion capturé
            capture_effectuee = True
            return True, capture_effectuee

    return True, capture_effectuee



def verifier_fin_jeu():
    global compteur_rouge, compteur_bleu
    rouges = [p for p in pions if p.couleur == ROUGE]
    bleus = [p for p in pions if p.couleur == BLEU]
    if not rouges:
        compteur_bleu += 1
        return "Bleu"
    if not bleus:
        compteur_rouge += 1
        return "Rouge"
    return None


# Afficher le message du tour
def afficher_tour(joueur):
    font = pygame.font.SysFont(None, 40)  # Augmenter la taille de la police à 72
    texte = font.render(f"C'est le tour des {joueur}", True, GRIS_CLAIR)
    ecran.blit(texte, (LARGEUR_FENETRE // 2 - texte.get_width() // 2, 20))


# Fonction pour la fenêtre de démarrage
def afficher_menu_principal():
    ecran.fill(BLANC)
    font = pygame.font.SysFont(None, 74)
    titre = font.render("Jeu de Dames", True, NOIR)
    ecran.blit(titre, (LARGEUR_FENETRE // 2 - titre.get_width() // 2, HAUTEUR_ECRAN // 4))

    # Bouton "Lancer le jeu"
    bouton_jouer = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2, 300, 50)
    pygame.draw.rect(ecran, VERT, bouton_jouer)
    texte_jouer = pygame.font.SysFont(None, 36).render("Lancer le jeu", True, NOIR)
    ecran.blit(texte_jouer, (bouton_jouer.centerx - texte_jouer.get_width() // 2, bouton_jouer.centery - texte_jouer.get_height() // 2))

    # Bouton "Stats"
    bouton_stats = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2 + 100, 300, 50)
    pygame.draw.rect(ecran, BLEU, bouton_stats)
    texte_stats = pygame.font.SysFont(None, 36).render("Stats", True, NOIR)
    ecran.blit(texte_stats, (bouton_stats.centerx - texte_stats.get_width() // 2, bouton_stats.centery - texte_stats.get_height() // 2))

    # Bouton "Quitter"
    bouton_quitter = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2 + 200, 300, 50)
    pygame.draw.rect(ecran, ROUGE, bouton_quitter)
    texte_quitter = pygame.font.SysFont(None, 36).render("Quitter", True, NOIR)
    ecran.blit(texte_quitter, (bouton_quitter.centerx - texte_quitter.get_width() // 2, bouton_quitter.centery - texte_quitter.get_height() // 2))

    pygame.display.flip()

    # Attente de l'entrée de l'utilisateur
    choix = None
    while choix is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if bouton_jouer.collidepoint(pos):
                    choix = 'jouer'
                elif bouton_quitter.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
                elif bouton_stats.collidepoint(pos):
                    showinfo(title="Stats", message=f"Les bleus ont gagné {compteur_bleu}x\n Les rouges ont gagné"
                                                    f" {compteur_rouge}x")
    return choix

def captures_possibles(pion):
    # Vérifier si le pion peut effectuer une autre capture après le déplacement
    i, j = (pion.x - debut_x - epaisseur_bordure) // taille_case, (pion.y - debut_y - epaisseur_bordure) // taille_case

    directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]  # Diagonales possibles
    for di, dj in directions:
        i_milieu = i + di
        j_milieu = j + dj
        i_final = i + 2 * di
        j_final = j + 2 * dj

        # Vérifier si la case intermédiaire est occupée par un pion adverse et si la case finale est vide
        if 0 <= i_milieu < 10 and 0 <= j_milieu < 10 and 0 <= i_final < 10 and 0 <= j_final < 10:
            pion_intermediaire = case_occupee((i_milieu, j_milieu))
            pion_final = case_occupee((i_final, j_final))
            if pion_intermediaire and pion_intermediaire.couleur != pion.couleur and not pion_final:
                return True  # Capture possible
    return False  # Pas de capture possible


# Afficher le menu principal
afficher_menu_principal()

# Boucle principale du jeu
running = True
pion_selectionne = None
tour = 'bleus'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Déselectionner tous les pions avant la sélection d'un nouveau
            for pion in pions:
                pion.selectionne = False

            if pion_selectionne:
                case_depart = case_cliquee((pion_selectionne.x, pion_selectionne.y))
                case_arrivee = case_cliquee(pos)

                # Vérifier la validité du mouvement et si une capture a eu lieu
                valide, capture_effectuee = mouvement_valide(case_depart, case_arrivee, pion_selectionne)

                if valide:
                    pion_selectionne.deplacer(case_arrivee)
                    if pion_selectionne.couleur == ROUGE and case_arrivee[1] == 9 or \
                            pion_selectionne.couleur == BLEU and case_arrivee[1] == 0:
                        pion_selectionne.promouvoir_en_reine()

                    # Si une capture a eu lieu et qu'il est encore possible de capturer, reste au tour actuel
                    if capture_effectuee:
                        # Vérifiez si d'autres captures sont possibles pour ce pion
                        if captures_possibles(pion_selectionne):
                            # Le joueur peut continuer à capturer
                            pion_selectionne = None
                        else:
                            # Aucun mouvement de capture supplémentaire, change de joueur
                            tour = 'bleus' if tour == 'rouges' else 'rouges'
                    else:
                        # Aucune capture, le tour passe au joueur suivant
                        tour = 'bleus' if tour == 'rouges' else 'rouges'

                    gagnant = verifier_fin_jeu()
                    if gagnant:
                        print(f"Félicitations aux {gagnant}s !")
                        time.sleep(2)
                        afficher_menu_principal()
                        dessiner_echiquier()
                        pions.clear()
                        initialiser_pion()

                    pion_selectionne = None
                else:
                    pion_selectionne = None
            else:
                for pion in pions:
                    if pion.contient_point(pos) and \
                            pion.couleur == (ROUGE if tour == 'rouges' else BLEU):
                        pion_selectionne = pion
                        pion.selectionne = True
                        break

    dessiner_echiquier()
    for pion in pions:
        pion.dessiner(ecran)

    afficher_tour(tour)
    pygame.display.flip()

pygame.quit()
sys.exit()