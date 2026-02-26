"""
    Main module of the ChickenVac3200®™©℗ game.
"""

import pygame
import random
import Entites
import Exceptions
import Moteur
from pygame import Color

# Initialize the Pygame modules.
try:
    pygame.init()
except pygame.error as e:
    print(Exceptions.ErreurPygameInitialisation(str(e)))
    raise SystemExit

# Initialize the sounds.
try:
    Sons = Moteur.Sons()
except Exceptions.FichierIntrouvableErreur as e:
    print(e)
    raise SystemExit

# Instantiation of the Music object.
Musique = Moteur.Musique()

# Change the default Pygame icon.
try:
    try:
        logo = pygame.image.load("logo.gif")
        pygame.display.set_icon(logo)
    except FileNotFoundError:
        raise Exceptions.FichierIntrouvableErreur("logo.gif")
except Exceptions.FichierIntrouvableErreur as e:
    print(e)
    raise SystemExit

# Declare and initialize constants and variables.
NB_POULETS_INITIAL = 20
LARGEUR_FENETRE = 1024
HAUTEUR_FENETRE = 768
TEMPS_PARTIE = 64
champ = 1
fin = False
intro_terminee = False
liste_entite = []
musique_intro = True
nb_poulets = NB_POULETS_INITIAL
nouvelle_partie = True
partie_intro = True
partie_echouee = False
partie_en_cours = False
partie_reussie = False
temps_restant = 0

# Open the Pygame window.
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

# Define the window for the different classes.
Entites.Joueur.set_fenetre(fenetre)
Entites.Poulet.set_fenetre(fenetre)
Moteur.Affichage.set_fenetre(fenetre)
Moteur.Boutons.set_fenetre(fenetre)

# Define the title at the top of the window.
pygame.display.set_caption("ChickenVac3200®™©℗") 

# To control the frequency of the scenes.
horloge = pygame.time.Clock()

# For reference during the game.
debut_partie = pygame.time.get_ticks()

# Instantiating objects for text display.
affichage_poulet = Moteur.Affichage(5, 5, "Poulets restants: 0", 26)
affichage_temps = Moteur.Affichage(873, 5, "Temps restants: 0", 26)
affichage_champ = Moteur.Affichage(473, 5, "Champ: 0", 26)
affichage_partie_echouee = Moteur.Affichage(250, 150, "Bel essai, mais tu n'as pas su ...RESTER EN VIE...", 36)
affichage_partie_echouee_champ = Moteur.Affichage(380, 180, "Tu as échoué au champ 0", 36)
affichage_partie_reussie = Moteur.Affichage(305, 150, "Bravo ! Tu as bien su ...RESTER EN VIE...", 36)
affichage_partie_reussie_champ = Moteur.Affichage(395, 180, "Tu as réussi le champ 0", 36)
liste_affichage_intro = [Moteur.Affichage(60, 50, "An 3200. Les temps ont changés ... et les conditions de travail aussi. Il", 36), 
                         Moteur.Affichage(60, 80, "faut récolter les poulets selon les méthodes ancestrales avant qu'ils soient", 36),
                         Moteur.Affichage(60, 110, "trop mûrs. Quand ils se gâtent, ces fameux poulets génétiquement modifiés", 36),
                         Moteur.Affichage(60, 140, "de l'empire du Régime International Communiste Agréé Réformé Des Oiseaux", 36),
                         Moteur.Affichage(60, 170, "(R.I.C.A.R.D.O.) ont tendance à déclencher une réaction en chaîne interne", 36),
                         Moteur.Affichage(60, 200, "d'auto-convertion des graisses en nitroglycérine et à exploser. Sers-toi du", 36),
                         Moteur.Affichage(60, 230, "bouton CTRL GAUCHE et des flèches du clavier pour faire ton travail. Clic", 36),
                         Moteur.Affichage(60, 260, "sur TRAVAILLER quand tu es prêt. Il faut gagner sa vie, en tentant de", 36),
                         Moteur.Affichage(60, 290, "...RESTER EN VIE...", 36),
                         Moteur.Affichage(10, 700, "ChickenVac3200®™©℗               Tous droits réservés  |  Brevets en instance", 40),
                         Moteur.Affichage(461, 735, "!*!*! Développé au Canada !*!*!   |   Compilé en Chine", 26)]

# Animation loop and game logic.
while not fin :

    # Find the next event to process.
    event = pygame.event.poll()

    # Check if the user clicked on the window close button?
    if event.type == pygame.QUIT:

        # End of the game loop.
        fin = True
    else :

        # Introduction to the game.
        if (partie_intro == True):
            fenetre.fill(Color('black'))
            for elements in liste_affichage_intro:
                elements.dessiner()
            bouton_debut_partie = Moteur.Boutons(pygame.Rect(450, 350, 160, 60), "Travailler")
            bouton_debut_partie.dessiner()
            bouton_debut_partie.cliquer()
            if (musique_intro == True):
                try:
                    Musique.jouer_musique_intro()
                except Exceptions.FichierIntrouvableErreur as e:
                    print(e)
                    raise SystemExit
                musique_intro = False
            if (bouton_debut_partie.cliquer() == True):
                partie_intro = False
                debut_partie = pygame.time.get_ticks()
                Musique.arreter_musique()
                intro_terminee = True

        # Initializing the first game.
        if (intro_terminee == True):
            temps_ecoule, temps_restant = Moteur.calculer_temps(debut_partie, TEMPS_PARTIE)

            # Initializing a game: instantiation of game entities and some initialization for the game.
            if (partie_en_cours == False) and (nouvelle_partie == True):
                try:
                    liste_entite = Moteur.generer_poulets(nb_poulets, LARGEUR_FENETRE, HAUTEUR_FENETRE)
                except Moteur.Exceptions.FichierIntrouvableErreur as e:
                    print(e)
                    raise SystemExit
                joueur = Entites.Joueur(pygame.Rect((LARGEUR_FENETRE/2, HAUTEUR_FENETRE/2), (40,40)))
                try:
                    Musique.jouer_musique_jeu()
                except Exceptions.FichierIntrouvableErreur as e:
                    print(e)
                    raise SystemExit          
                nouvelle_partie = False
                partie_en_cours = True
            
            # During a game: checking whether a game was won or lost.
            if (len(liste_entite) == 0) and (temps_restant > 0):
                partie_reussie = True
            elif (len(liste_entite) > 0) and (temps_restant == 0):
                partie_echouee = True

            # During a game: normal game operation.
            if (partie_en_cours == True) :

                # Player actions and movement.
                Moteur.gerer_joueur(joueur, event)
                liste_entite = Moteur.enlever_poulets_capture(joueur, liste_entite)

                # Make the chickens moving.
                Moteur.maj_poulets(liste_entite)

                # Interface text updated during gameplay.
                Moteur.maj_texte([affichage_poulet, affichage_temps, affichage_champ], [f"Poulets restants: {len(liste_entite)}", f"Temps restant: {temps_restant}", f"Champ: {champ}"])

            # During a game: normal game operation.
            if (partie_echouee == False) and (partie_reussie == False):
                Moteur.dessiner_jeu(fenetre, joueur, liste_entite, [affichage_poulet, affichage_temps, affichage_champ])
            
            # Game over.
            elif (partie_echouee == True):
                if (partie_en_cours == True):
                    Sons.son_explosion.play()
                    partie_en_cours = False
                fenetre.fill(Color('red'))
                liste_entite = []
                Musique.arreter_musique()
                affichage_partie_echouee_champ.mettre_a_jour(f"Tu as échoué au champ {champ}")
                affichage_partie_echouee.dessiner()
                affichage_partie_echouee_champ.dessiner()
                bouton_rejouer = Moteur.Boutons(pygame.Rect(450, 350, 160, 60), "Réessayer")
                bouton_rejouer.dessiner()
                bouton_rejouer.cliquer()
                
                # Game failed: actions of the "réessayer" button.
                if (bouton_rejouer.cliquer() == True):
                    nouvelle_partie = True
                    partie_echouee = False
                    nb_poulets = NB_POULETS_INITIAL
                    champ = 1
                    debut_partie = pygame.time.get_ticks()
            
            # Game won.
            if (partie_reussie == True):
                fenetre.fill(Color('#3CB043'))
                affichage_partie_reussie_champ.mettre_a_jour(f"Tu as réussi le champ {champ}")
                affichage_partie_reussie.dessiner()
                affichage_partie_reussie_champ.dessiner()
                bouton_champ_suivant = Moteur.Boutons(pygame.Rect(420, 350, 220, 60), "Champ suivant")
                bouton_champ_suivant.dessiner()
                bouton_champ_suivant.cliquer()
                if (partie_en_cours == True):
                    Musique.arreter_musique()
                    try:
                        Musique.jouer_musique_victoire()
                    except Exceptions.FichierIntrouvableErreur as e:
                        print(e)
                        raise SystemExit
                    partie_en_cours = False

                # Game won : actions of the "champ suivant" button.
                if (bouton_champ_suivant.cliquer() == True):
                    nouvelle_partie = True
                    partie_reussie = False
                    champ = champ + 1
                    nb_poulets = nb_poulets + 5
                    debut_partie = pygame.time.get_ticks()
                    Musique.arreter_musique()

        # Update the graphics window.
        pygame.display.flip() 

        # To animate with 60 frames per second.
        horloge.tick(60) 

# Ends pygame.
pygame.quit() 