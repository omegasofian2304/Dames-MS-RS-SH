from tkinter.messagebox import showinfo

from backend import (pions, COULEURS, img_pion, TAILLE_PION, TAILLE_CASE, EPAISSEUR_BORDURE, MARGE_X, MARGE_Y, Pion, \
    ecran, LARGEUR_FENETRE, HAUTEUR_ECRAN, stats, case_occupee, case_cliquee, captures_possibles, effectuer_captures_multiples,
    mouvement_valide, verifier_fin_jeu, colorier_pion, pion_rouge, pion_bleu)
import time
import pygame
import sys

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

# Fonction pour afficher le tour actuel
def afficher_tour(joueur):
    """
    Affiche un message indiquant le tour du joueur actuel.
    """
    font = pygame.font.SysFont(None, 40)
    texte = font.render(f"C'est le tour des {joueur}", True, COULEURS["GRIS_CLAIR"])
    ecran.blit(texte, (LARGEUR_FENETRE // 2 - texte.get_width() // 2, 20))

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
