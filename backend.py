# Titre : backend.py
# Auteur : Sofian, Rodrigo, Milo
# Date : 13.01.2025

# Importation des bibliothèques nécessaires
import pygame

# Initialisation de Pygame
pygame.init()

# Définition des couleurs (RGB)
COULEURS = {
    "BLANC": (255, 255, 255),
    "BRUN": (139, 69, 19),
    "NOIR": (0, 0, 0),
    "VERT": (0, 120, 0),
    "BLEU": (30, 30, 255),
    "ROUGE": (255, 0, 0),
    "GRIS_CLAIR": (200, 200, 200),
}

# Dimensions des éléments du plateau
TAILLE_CASE = 75
TAILLE_PION = 50
EPAISSEUR_BORDURE = 15

# Configuration de la fenêtre de jeu (plein écran)
LARGEUR_FENETRE, HAUTEUR_ECRAN = pygame.display.Info().current_w, pygame.display.Info().current_h
ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_ECRAN))

# Calcul des marges pour centrer le plateau
MARGE_X = (LARGEUR_FENETRE - 10 * TAILLE_CASE - 2 * EPAISSEUR_BORDURE) // 2
MARGE_Y = (HAUTEUR_ECRAN - 10 * TAILLE_CASE - 2 * EPAISSEUR_BORDURE) // 2

# Chargement et redimensionnement de l'image des pions
img_pion = pygame.image.load("img\\MA-24_pion.png")
img_pion = pygame.transform.scale(img_pion, (TAILLE_PION, TAILLE_PION))

# Variables de statistiques des parties
stats = {"BLEU": 0, "ROUGE": 0}

# Fonction pour colorier l'image d'un pion
def colorier_pion(image, couleur):
    """
    Applique une teinte de couleur sur une image de pion.
    """
    overlay = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)
    overlay.fill(couleur)
    image_coloree = image.copy()
    image_coloree.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return image_coloree

# Initialisation des images colorées des pions
pion_bleu = colorier_pion(img_pion, COULEURS["BLEU"])
pion_rouge = colorier_pion(img_pion, COULEURS["ROUGE"])

# Classe pour représenter un pion
class Pion:
    """
    Classe représentant un pion sur le plateau.
    """

    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.selectionne = False
        self.est_reine = False

    def dessiner(self, surface):
        """
        Affiche le pion sur l'écran.
        """
        img = pion_bleu if self.couleur == COULEURS["BLEU"] else pion_rouge
        surface.blit(img, (self.x - TAILLE_PION // 2, self.y - TAILLE_PION // 2))
        if self.selectionne:
            pygame.draw.circle(surface, COULEURS["GRIS_CLAIR"], (self.x, self.y), TAILLE_PION // 2 + 5, 3)
        if self.est_reine:
            pygame.draw.circle(surface, COULEURS["GRIS_CLAIR"], (self.x, self.y), TAILLE_PION // 4)

    def contient_point(self, pos):
        """
        Vérifie si un point donné (clic souris) est dans la zone du pion.
        """
        dx, dy = pos[0] - self.x, pos[1] - self.y
        return dx ** 2 + dy ** 2 <= (TAILLE_PION // 2) ** 2

    def deplacer(self, nouvelle_case):
        """
        Déplace le pion à une nouvelle position calculée.
        """
        i, j = nouvelle_case
        self.x = MARGE_X + EPAISSEUR_BORDURE + i * TAILLE_CASE + TAILLE_CASE // 2
        self.y = MARGE_Y + EPAISSEUR_BORDURE + j * TAILLE_CASE + TAILLE_CASE // 2

    def promouvoir_en_reine(self):
        """
        Promeut le pion en reine.
        """
        self.est_reine = True

# Liste pour stocker tous les pions
pions = []

# Déterminer la case cliquée
def case_cliquee(pos):
    """
    Retourne la position (colonne, ligne) de la case cliquée ou None si le clic est hors du plateau.
    """
    x, y = pos
    if MARGE_X + EPAISSEUR_BORDURE <= x < MARGE_X + EPAISSEUR_BORDURE + 10 * TAILLE_CASE and \
            MARGE_Y + EPAISSEUR_BORDURE <= y < MARGE_Y + EPAISSEUR_BORDURE + 10 * TAILLE_CASE:
        colonne = (x - MARGE_X - EPAISSEUR_BORDURE) // TAILLE_CASE
        ligne = (y - MARGE_Y - EPAISSEUR_BORDURE) // TAILLE_CASE
        print(f"Case cliquée : colonne {colonne}, ligne {ligne}")  # DEBUG
        return int(colonne), int(ligne)
    print("Clic hors plateau")  # DEBUG
    return None

# Vérifier si une case est occupée par un pion
def case_occupee(case):
    """
    Vérifie si une case donnée est occupée par un pion.
    Retourne le pion trouvé ou None si la case est vide.
    """
    colonne, ligne = case
    for pion in pions:
        if pion.x == MARGE_X + EPAISSEUR_BORDURE + colonne * TAILLE_CASE + TAILLE_CASE // 2 and \
                pion.y == MARGE_Y + EPAISSEUR_BORDURE + ligne * TAILLE_CASE + TAILLE_CASE // 2:
            return pion
    return None

# Vérifier les captures possibles
def captures_possibles(case, pion_selectionne):
    """
    Retourne une liste des cases d'arrivée possibles pour une capture depuis la case donnée.
    """
    captures = []
    colonne_depart, ligne_depart = case
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Haut gauche, haut droite, bas gauche, bas droite

    for direction in directions:
        colonne_arrivee = colonne_depart + direction[0]
        ligne_arrivee = ligne_depart + direction[1]
        case_arrivee = (colonne_arrivee, ligne_arrivee)

        # Vérifier que la case d'arrivée est dans les limites
        if 0 <= colonne_arrivee < 10 and 0 <= ligne_arrivee < 10:
            colonne_milieu = (colonne_depart + colonne_arrivee) // 2
            ligne_milieu = (ligne_depart + ligne_arrivee) // 2
            case_milieu = (colonne_milieu, ligne_milieu)
            pion_intermediaire = case_occupee(case_milieu)

            # Vérifier si une capture est possible
            if (
                pion_intermediaire and
                pion_intermediaire.couleur != pion_selectionne.couleur and
                not case_occupee(case_arrivee)
            ):
                captures.append(case_arrivee)

    return captures

# Effectuer des captures multiples
def effectuer_captures_multiples(pion_selectionne, case_depart):
    """
    Permet d'enchaîner les captures multiples si possible.
    """
    case_actuelle = case_depart
    while True:
        captures = captures_possibles(case_actuelle, pion_selectionne)
        if not captures:
            break  # Arrêter si aucune capture possible

        # Supposons que le joueur choisit automatiquement la première capture possible
        case_suivante = captures[0]
        colonne_depart, ligne_depart = case_actuelle
        colonne_arrivee, ligne_arrivee = case_suivante

        # Identifier le pion capturé
        colonne_milieu = (colonne_depart + colonne_arrivee) // 2
        ligne_milieu = (ligne_depart + ligne_arrivee) // 2
        pion_intermediaire = case_occupee((colonne_milieu, ligne_milieu))

        if pion_intermediaire:
            pions.remove(pion_intermediaire)  # Supprimer le pion capturé
            print(f"Pion capturé à la case {(colonne_milieu, ligne_milieu)}")

        # Déplacer le pion sur la nouvelle case
        pion_selectionne.deplacer(case_suivante)
        case_actuelle = case_suivante

# Vérifier si un mouvement est valide
def mouvement_valide(case_depart, case_arrivee, pion_selectionne):
    """
    Vérifie si un mouvement est valide pour un pion donné.
    """
    print(f"Départ : {case_depart}, Arrivée : {case_arrivee}")  # DEBUG
    capture_effectuee = False
    mouvement_multiple = False

    # Décomposition des coordonnées de départ et d'arrivée
    colonne_depart, ligne_depart = case_depart
    colonne_arrivee, ligne_arrivee = case_arrivee

    # Vérifier que le mouvement est bien en diagonale
    if abs(colonne_arrivee - colonne_depart) != abs(ligne_arrivee - ligne_depart):
        print("Mouvement non diagonal")  # DEBUG
        return False, capture_effectuee, mouvement_multiple

    # Vérifier si la case d'arrivée est une case valide (noire)
    if (colonne_arrivee + ligne_arrivee) % 2 == 0:
        print("Case arrivée non valide (pas une case noire)")  # DEBUG
        return False, capture_effectuee, mouvement_multiple

    # Vérifier si la case d'arrivée est déjà occupée
    pion_occupe = case_occupee(case_arrivee)
    if pion_occupe:
        print("Case arrivée occupée")  # DEBUG
        return False, capture_effectuee, mouvement_multiple

    # Déterminer la direction d'avancement en fonction de la couleur
    if pion_selectionne.couleur == COULEURS["ROUGE"]:  # Rouge monte
        avance_correctement = (ligne_arrivee > ligne_depart)
    else:  # Bleu descend
        avance_correctement = (ligne_arrivee < ligne_depart)

    # Mouvement simple vers l'avant (1 case diagonale)
    if abs(colonne_arrivee - colonne_depart) == 1 and avance_correctement:
        print("Mouvement simple valide")  # DEBUG
        return True, capture_effectuee, mouvement_multiple

    # Capture en diagonale (2 cases en avant ou en arrière)
    if abs(colonne_arrivee - colonne_depart) == 2 and abs(ligne_arrivee - ligne_depart) == 2:
        colonne_milieu = (colonne_depart + colonne_arrivee) // 2
        ligne_milieu = (ligne_depart + ligne_arrivee) // 2
        pion_intermediaire = case_occupee((colonne_milieu, ligne_milieu))
        if pion_intermediaire and pion_intermediaire.couleur != pion_selectionne.couleur:
            pions.remove(pion_intermediaire)
            capture_effectuee = True
            print("Capture valide effectuée")  # DEBUG
            return True, capture_effectuee, mouvement_multiple

    # Recul interdit sans capture
    if not avance_correctement:
        print("Recul interdit sans capture")  # DEBUG
        return False, capture_effectuee, mouvement_multiple

    # Aucun autre mouvement valide
    print("Mouvement non valide")  # DEBUG
    return False, capture_effectuee, mouvement_multiple

# Vérifier la fin du jeu
def verifier_fin_jeu():
    """
    Vérifie si la partie est terminée.
    Retourne "BLEU" ou "ROUGE" si un camp a gagné, ou None si la partie continue.
    """
    global stats
    rouges_restants = [p for p in pions if p.couleur == COULEURS["ROUGE"]]
    bleus_restants = [p for p in pions if p.couleur == COULEURS["BLEU"]]
    if not rouges_restants:
        stats["BLEU"] += 1
        return "BLEU"
    if not bleus_restants:
        stats["ROUGE"] += 1
        return "ROUGE"
    return None


