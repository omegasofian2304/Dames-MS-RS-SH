#titre : dame.py
#auteur : Sofian
#date : 16.12.2024

# Importation des bibliothèques nécessaires
from tkinter.messagebox import showinfo
import time
import pygame
import sys

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
pygame.display.set_caption("Plateau de Dames 10x10")

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


# Initialisation des pions sur le plateau
def initialiser_pions():
    """
    Place les pions rouges et bleus sur leurs positions initiales.
    """
    # Pions rouges (en haut)
    for colonne in range(10):
        for ligne in range(4):
            if (colonne + ligne) % 2 == 1:  # Les cases noires uniquement
                x = MARGE_X + EPAISSEUR_BORDURE + colonne * TAILLE_CASE + TAILLE_CASE // 2
                y = MARGE_Y + EPAISSEUR_BORDURE + ligne * TAILLE_CASE + TAILLE_CASE // 2
                pions.append(Pion(x, y, COULEURS["ROUGE"]))

    # Pions bleus (en bas)
    for colonne in range(10):
        for ligne in range(6, 10):
            if (colonne + ligne) % 2 == 1:  # Les cases noires uniquement
                x = MARGE_X + EPAISSEUR_BORDURE + colonne * TAILLE_CASE + TAILLE_CASE // 2
                y = MARGE_Y + EPAISSEUR_BORDURE + ligne * TAILLE_CASE + TAILLE_CASE // 2
                pions.append(Pion(x, y, COULEURS["BLEU"]))


initialiser_pions()


# Fonction pour dessiner l'échiquier
def dessiner_echiquier():
    """
    Dessine le plateau de jeu avec ses cases noires et blanches.
    """
    ecran.fill(COULEURS["BRUN"])  # Fond vert
    pygame.draw.rect(ecran, COULEURS["NOIR"],
                     (MARGE_X, MARGE_Y, 10 * TAILLE_CASE + 2 * EPAISSEUR_BORDURE,
                      10 * TAILLE_CASE + 2 * EPAISSEUR_BORDURE))  # Bordure du plateau

    # Dessiner les cases du plateau
    for colonne in range(10):
        for ligne in range(10):
            x = MARGE_X + colonne * TAILLE_CASE + EPAISSEUR_BORDURE
            y = MARGE_Y + ligne * TAILLE_CASE + EPAISSEUR_BORDURE
            couleur_case = COULEURS["BRUN"] if (colonne + ligne) % 2 == 1 else COULEURS["BLANC"]
            pygame.draw.rect(ecran, couleur_case, (x, y, TAILLE_CASE, TAILLE_CASE))


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


# faut faire une boucle qui fait qu'on peut encore manger tant qu'une variable est True
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


def afficher_tour(joueur):
    """
    Affiche un message indiquant le tour du joueur actuel.
    """
    font = pygame.font.SysFont(None, 40)
    texte = font.render(f"C'est le tour des {joueur}", True, COULEURS["GRIS_CLAIR"])
    ecran.blit(texte, (LARGEUR_FENETRE // 2 - texte.get_width() // 2, 20))


# Fonction pour afficher le menu principal
def afficher_menu_principal():
    """
    Affiche le menu principal avec les options : Jouer, Voir les stats et Quitter.
    """
    ecran.fill(COULEURS["BRUN"])
    font_titre = pygame.font.SysFont(None, 74)
    titre = font_titre.render("Jeu de Dames", True, COULEURS["NOIR"])
    ecran.blit(titre, (LARGEUR_FENETRE // 2 - titre.get_width() // 2, HAUTEUR_ECRAN // 4))

    # Bouton "Lancer le jeu"
    bouton_jouer = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2, 300, 50)
    pygame.draw.rect(ecran, COULEURS["VERT"], bouton_jouer)
    texte_jouer = pygame.font.SysFont(None, 36).render("Lancer le jeu", True, COULEURS["NOIR"])
    ecran.blit(texte_jouer, (
    bouton_jouer.centerx - texte_jouer.get_width() // 2, bouton_jouer.centery - texte_jouer.get_height() // 2))

    # Bouton "Stats"
    bouton_stats = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2 + 100, 300, 50)
    pygame.draw.rect(ecran, COULEURS["BLEU"], bouton_stats)
    texte_stats = pygame.font.SysFont(None, 36).render("Stats", True, COULEURS["NOIR"])
    ecran.blit(texte_stats, (
    bouton_stats.centerx - texte_stats.get_width() // 2, bouton_stats.centery - texte_stats.get_height() // 2))

    # Bouton "Quitter"
    bouton_quitter = pygame.Rect(LARGEUR_FENETRE // 2 - 150, HAUTEUR_ECRAN // 2 + 200, 300, 50)
    pygame.draw.rect(ecran, COULEURS["ROUGE"], bouton_quitter)
    texte_quitter = pygame.font.SysFont(None, 36).render("Quitter", True, COULEURS["NOIR"])
    ecran.blit(texte_quitter, (
    bouton_quitter.centerx - texte_quitter.get_width() // 2, bouton_quitter.centery - texte_quitter.get_height() // 2))

    pygame.display.flip()

    # Gestion des événements du menu
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
                    showinfo(
                        title="Stats",
                        message=f"Les bleus ont gagné {stats['BLEU']} fois\nLes rouges ont gagné {stats['ROUGE']} fois"
                    )
    return choix


# Afficher le menu principal
afficher_menu_principal()

# Boucle principale du jeu avec toutes les vérifications nécessaires
jeu_en_cours = True
pion_selectionne = None
joueur_actuel = 'bleus'  # Le joueur actif

while jeu_en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            jeu_en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                jeu_en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            position_clic = pygame.mouse.get_pos()

            # Déselectionner tous les pions avant une nouvelle sélection
            for pion in pions:
                pion.selectionne = False

            if pion_selectionne:  # Si un pion est déjà sélectionné
                # Déterminer les cases de départ et d'arrivée
                case_depart = case_cliquee((pion_selectionne.x, pion_selectionne.y))
                case_arrivee = case_cliquee(position_clic)

                # Vérifier la validité du mouvement avec les règles avancées
                valide_mouvement, capture_effectuee, mouvement_multiple = mouvement_valide(case_depart, case_arrivee, pion_selectionne)

                if valide_mouvement:
                    # Déplacer le pion valide
                    pion_selectionne.deplacer(case_arrivee)

                    # Vérifier si la promotion doit s'appliquer
                    if pion_selectionne.couleur == COULEURS["ROUGE"] and case_arrivee[1] == 9 or \
                            pion_selectionne.couleur == COULEURS["BLEU"] and case_arrivee[1] == 0:
                        pion_selectionne.promouvoir_en_reine()

                    # Gérer les captures
                    if capture_effectuee:
                        print("Capture effectuée.")
                        # Gérer les captures multiples
                        effectuer_captures_multiples(pion_selectionne, case_arrivee)

                    # Si aucune capture supplémentaire, passer au joueur suivant
                    if not capture_effectuee or not captures_possibles(case_arrivee, pion_selectionne):
                        joueur_actuel = 'bleus' if joueur_actuel == 'rouges' else 'rouges'

                    # Vérifier la fin de la partie après le mouvement
                    gagnant = verifier_fin_jeu()
                    if gagnant:
                        print(f"Félicitations aux {gagnant}s !")
                        time.sleep(2)
                        afficher_menu_principal()
                        dessiner_echiquier()
                        pions.clear()
                        initialiser_pions()
                    pion_selectionne = None
                else:
                    print("Mouvement invalide.")
                    pion_selectionne = None
            else:  # Sinon, tenter de sélectionner un pion
                for pion in pions:
                    if pion.contient_point(position_clic) and \
                            pion.couleur == (COULEURS["ROUGE"] if joueur_actuel == 'rouges' else COULEURS["BLEU"]):
                        pion_selectionne = pion
                        pion.selectionne = True
                        break

    # Redessiner l'échiquier et les pions
    dessiner_echiquier()
    for pion in pions:
        pion.dessiner(ecran)

    # Afficher le message indiquant le joueur actuel
    afficher_tour(joueur_actuel)
    pygame.display.flip()

pygame.quit()
sys.exit()