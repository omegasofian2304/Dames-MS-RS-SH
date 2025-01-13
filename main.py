# Titre : main.py
# Auteur : Milo, Rodrigo, Sofian
# Date : 13.01.2025

from frontend import (
    COULEURS, Pion, pions, case_occupee, case_cliquee, captures_possibles,
    colorier_pion, effectuer_captures_multiples, mouvement_valide, afficher_tour,
    afficher_menu_principal, dessiner_echiquier, verifier_fin_jeu, initialiser_pions, ecran)
import pygame
import time
import sys

# Initialisation du jeu
jeu_en_cours = True
pion_selectionne = None
joueur_actuel = 'bleus'  # Le joueur actif

# Affichage du menu principal
choix = afficher_menu_principal()
if choix != 'jouer':
    pygame.quit()
    sys.exit()

# Initialisation du plateau
initialiser_pions()

def gerer_evenement_souris(position_clic):
    """
    Gère les événements de clic souris pour sélectionner ou déplacer un pion.
    """
    global pion_selectionne, joueur_actuel

    # Déselectionner tous les pions avant une nouvelle sélection
    for pion in pions:
        pion.selectionne = False

    if pion_selectionne:  # Si un pion est déjà sélectionné
        # Déterminer les cases de départ et d'arrivée
        case_depart = case_cliquee((pion_selectionne.x, pion_selectionne.y))
        case_arrivee = case_cliquee(position_clic)

        # Vérifier la validité du mouvement avec les règles avancées
        valide_mouvement, capture_effectuee, _ = mouvement_valide(case_depart, case_arrivee, pion_selectionne)

        if valide_mouvement:
            # Déplacer le pion valide
            pion_selectionne.deplacer(case_arrivee)

            # Vérifier si la promotion doit s'appliquer
            if (
                pion_selectionne.couleur == COULEURS["ROUGE"] and case_arrivee[1] == 9 or
                pion_selectionne.couleur == COULEURS["BLEU"] and case_arrivee[1] == 0
            ):
                pion_selectionne.promouvoir_en_reine()

            # Gérer les captures
            if capture_effectuee:
                effectuer_captures_multiples(pion_selectionne, case_arrivee)

            # Passer au joueur suivant si aucune capture supplémentaire
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

# Boucle principale du jeu
while jeu_en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            jeu_en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                jeu_en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_evenement_souris(pygame.mouse.get_pos())

    # Redessiner l'échiquier et les pions
    dessiner_echiquier()
    for pion in pions:
        pion.dessiner(ecran)

    # Afficher le message indiquant le joueur actuel
    afficher_tour(joueur_actuel)
    pygame.display.flip()

pygame.quit()
sys.exit()
