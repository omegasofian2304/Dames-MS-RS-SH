import pygame
pygame.init()

nb_case=1
nb_ligne=1
screen = pygame.display.set_mode((800, 800))
def afficher_damier():
    for h in range(10):
        global nb_ligne
        global nb_case
        for i in range(10):

            x = i * 80
            couleur = (65, 42, 42) if nb_case % 2 == 0 else (245, 245, 245)
            pygame.draw.rect(screen, couleur, (x, -80+(nb_ligne*80), 80, 80))
            nb_case=nb_case+1
        nb_case = nb_case + 1

        nb_ligne=nb_ligne+1
afficher_damier()
running = True
while running:
    # Récupérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter pygame
pygame.quit()