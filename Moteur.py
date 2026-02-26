"""
    Module which contains certain classes and functions of a more "mechanical" nature for the operation of the game.
"""

import Entites
import Exceptions
import pygame
import random
from pygame import Color
from Exceptions import FichierIntrouvableErreur


class Affichage:
    """ An object represents text that may or may not be animated within a Pygame window.

	The entity is inscribed within the bounding rectangle defined by r. 
        r : pygame.Rect       The encompassing rectangle.
    """

    @staticmethod
    def set_fenetre(fenetre):
        """ Set the class variable f that represents the graphics window.

            window : pygame.Surface
        """
        Affichage.f = fenetre

    def __init__(self, x, y, texte, taille):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, taille)
        self.t = texte

    def mettre_a_jour(self, texte):
        """ Method for updating the displayed text.
        """

        self.t = texte

    def dessiner(self):
        """ Method for drawing text on the window.

	    The text is inscribed within the bounding rectangle defined by the object variable `r` in a Pygame window.
        """

        texte = self.font.render(self.t, True, (255, 255, 255))
        self.f.blit(texte, (self.x, self.y))


class Boutons():
    """ An object represents a button in a Pygame window.

	The entity is inscribed within the bounding rectangle defined by r.
        r : pygame.Rect       The encompassing rectangle.
    """

    @staticmethod
    def set_fenetre(fenetre):
        """ Set the class variable f that represents the graphics window.

            window : pygame.Surface
        """
        Boutons.f = fenetre

    def __init__(self, rectangle, texte):
        self.r = rectangle
        self.t = texte
    
    def cliquer(self):
        """ A method that allows you to know if the mouse click is on the button.
        """

        souris_position = pygame.mouse.get_pos()
        souris_clic = pygame.mouse.get_pressed()
        return self.r.collidepoint(souris_position) and souris_clic[0]

    def dessiner(self):
        """ Draw a button.

	    The button is inscribed within the bounding rectangle defined by the object variable `r` in a Pygame window.
        """
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(Boutons.f, Color('gray'), self.r, border_radius=10)
        pygame.draw.rect(Boutons.f, Color('black'), self.r, 2, border_radius=10)
        bouton_texte = font.render(self.t, True, Color('black'))
        texte_rect = bouton_texte.get_rect(center=self.r.center)
        Boutons.f.blit(bouton_texte, texte_rect)


class Sons:
    """ A class that allows you to manage different sounds simply and in one place.
    """

    def __init__(self):
        """ A method that allows the initialization of audio functions and sound effects.
        """
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(Exceptions.ErreurPygameInitialisation(str(e)))
            raise SystemExit
        pygame.mixer.set_num_channels(128)
        fichiers_sons = {
            "son_aspirateur": "vacuum.wav",
            "son_poulet_cot": "poulet_cot.wav",
            "son_poulet_cri": "poulet_cri.wav",
            "son_explosion": "explosion.mp3"
        }
        for nom, fichier in fichiers_sons.items():
            try:
                setattr(Sons, nom, pygame.mixer.Sound(fichier))
            except FileNotFoundError:
                raise Exceptions.FichierIntrouvableErreur(fichier)

        # Set the volume of the sounds.
        Sons.son_aspirateur.set_volume(0.1)
        Sons.son_poulet_cot.set_volume(0.3)
        Sons.son_explosion.set_volume(0.5)


class Musique:
    """ A class that allows you to easily manage different music files in one place.
    """

    def __init__(self):
        pass

    def jouer_musique(self, fichier, volume=0.5, loops=0):
        """ Generic method for playing music. """
        try:
            pygame.mixer.music.load(fichier)
        except pygame.error:
            raise Exceptions.FichierIntrouvableErreur(fichier)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=loops)

    def jouer_musique_intro(self):
        """ A method that allows the introductory music to play.
        """

        self.jouer_musique("terminator.mp3", volume=0.3, loops=99)

    def jouer_musique_jeu(self):
        """ A method that allows music to be played during gameplay.
        """

        self.jouer_musique("stayin_alive.mp3", volume=0.2, loops=0)
    
    def jouer_musique_victoire(self):
        """ A method that allows the song of absolute victory to be played.
        """

        self.jouer_musique("robin_hood.mp3", volume=1, loops=0)
    
    def arreter_musique(self):
        """ A method that allows you to stop the music.
        """

        pygame.mixer.music.stop()


def calculer_temps(debut_partie, duree_partie):
    """ Return (temps_ecoule, temps_restant).
    """

    temps_actuel = pygame.time.get_ticks()
    temps_ecoule = (temps_actuel - debut_partie) // 1000
    temps_restant = max(0, duree_partie - temps_ecoule)
    return temps_ecoule, temps_restant


def dessiner_jeu(fenetre, joueur, poulets, textes, couleur_fond=Color('#3CB043')):
    """ Draw the background, the chickens, the player and the text.
    """
    fenetre.fill(couleur_fond)
    for obj in poulets:
        obj.dessiner()
    joueur.dessiner()
    for txt in textes:
        txt.dessiner()


def detection_collision(joueur, poulet):
    """ A function that checks for collisions between the vacuum cleaner nozzle and the chickens.

	Returns True or False.
    """

    joueur_rect = joueur.r.copy()
    joueur_rect.x += 20
    joueur_rect.y -= 40
    joueur_rect.width = 1
    joueur_rect.height = 1   
    return joueur_rect.colliderect(poulet.r)

def enlever_poulets_capture(joueur, poulets):
    """ Returns a new list of unvacuumed chickens. Updates player.vacuumed_chickens. Only captures if left CTRL is held down.
    """
    if pygame.K_LCTRL not in joueur.touche_enfoncee:
        return poulets

    capturees = 0
    nouvelle_liste = []
    for p in poulets:
        if detection_collision(joueur, p):
            Sons.son_poulet_cri.play()
            capturees += 1
        else:
            nouvelle_liste.append(p)
    
    joueur.poulets_aspires += capturees
    return nouvelle_liste


def generer_poulets(n, largeur_fenetre, hauteur_fenetre):
    return [Entites.Poulet(pygame.Rect((random.randint(0, largeur_fenetre - 40), random.randint(0, hauteur_fenetre - 40)), (40,40)), 32, "poulet", largeur_fenetre, hauteur_fenetre) for _ in range(n)]


def gerer_joueur(joueur, event):
    """ Controls the player: movement and vacuum cleaner.
    """

    joueur.evenements(event)

    # Play sound when CTRL is pressed
    if pygame.K_LCTRL in joueur.touche_enfoncee:
        Sons.son_aspirateur.play()
    
    joueur.deplacer()


def maj_poulets(poulets):
    """ Takes a list of chickens and calls faire_saut() and prochaine_scene() on each one.
    """
    for poulet in poulets:
        poulet.faire_saut()
        poulet.prochaine_scene()


def maj_texte(objets_texte, valeur):
    """ Function that updates the information displayed to the user.
    """

    for obj, val in zip(objets_texte, valeur):
        obj.mettre_a_jour(val)