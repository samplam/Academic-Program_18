"""
    Module that contains the classes of animated elements.
"""

import pygame
import random
from pygame import Color
import Moteur

# Initialiser les sons.
Sons = Moteur.Sons()

class Joueur():
    """ An object represents a player animated within a Pygame window.

	The entity is inscribed within the bounding rectangle defined by r. 
        r : pygame.Rect       The encompassing rectangle.
    """

    @staticmethod
    def set_fenetre(fenetre):
        """ Set the class variable f that represents the graphics window.

            window : pygame.Surface
        """
        Joueur.f = fenetre

    def __init__(self, rectangle):
        self.r = rectangle
        self.touche_enfoncee = set()
        self.poulets_aspires = 0

    def evenements(self, event):
        """ A method that allows the player's movements to be updated in the main program.
        
        """
        if event.type == pygame.KEYDOWN:
            self.touche_enfoncee.add(event.key)
        elif event.type == pygame.KEYUP:
            self.touche_enfoncee.discard(event.key)

    def deplacer(self):
        """ A method that allows you to calculate and limit the player's position in the main window.
        
        """
        touche = pygame.key.get_pressed()
        if ((pygame.K_LEFT in self.touche_enfoncee) and ((self.r.x + 20) > 0)):
            self.r.x = self.r.x - 3
        if ((pygame.K_RIGHT in self.touche_enfoncee) and ((self.r.x + 30) < Joueur.f.get_width())):
            self.r.x = self.r.x + 3
        if ((pygame.K_UP in self.touche_enfoncee) and ((self.r.y - 40) > 0)):
            self.r.y = self.r.y - 3
        if ((pygame.K_DOWN in self.touche_enfoncee) and ((self.r.y - 30) < Joueur.f.get_height())):
            self.r.y = self.r.y + 3

    def dessiner(self):
        """ Draw a player.

	    The player is inscribed within the bounding rectangle defined by the object variable `r` in a Pygame window.
        """
        pygame.draw.rect(Joueur.f, Color('#A67C52'), (self.r.x+(self.r.width/2), self.r.y-self.r.height, self.r.width/4, self.r.height)) # Dessiner l'aspirateur
        pygame.draw.rect(Joueur.f, Color('#000000'), (self.r.x+(self.r.width/2), self.r.y-self.r.height, self.r.width/4, self.r.height), width=2) # Dessiner l'aspirateur
        pygame.draw.rect(Joueur.f, Color('#AAB6C3'), (self.r.x-self.r.width, self.r.y-(self.r.height/4), self.r.width*2, self.r.height/2), border_radius=10) # Dessiner les épaules
        pygame.draw.rect(Joueur.f, Color('#000000'), (self.r.x-self.r.width, self.r.y-(self.r.height/4), self.r.width*2, self.r.height/2), width=2, border_radius=10) # Dessiner les épaules
        pygame.draw.ellipse(Joueur.f, Color('#A67C52'), (self.r.x-(self.r.width/2)-(2 * self.poulets_aspires), self.r.y, self.r.width + (4 * self.poulets_aspires), (self.r.height + (4 * self.poulets_aspires))/2)) # Dessiner le sac à dos
        pygame.draw.ellipse(Joueur.f, Color('#000000'), (self.r.x-(self.r.width/2)-(2 * self.poulets_aspires), self.r.y, self.r.width + (4 * self.poulets_aspires), (self.r.height + (4 * self.poulets_aspires))/2), width=2) # Dessiner le sac à dos pygame.draw.circle(Joueur.f, Color('#C8AD7F'), (self.r.x,self.r.y), self.r.width/2) # Dessiner le chapeau
        pygame.draw.circle(Joueur.f, Color('#C8AD7F'), (self.r.x,self.r.y), self.r.width/2) # Dessiner le chapeau
        pygame.draw.circle(Joueur.f, Color('#000000'), (self.r.x,self.r.y), self.r.width/2, width=2) # Dessiner le chapeau
        pygame.draw.circle(Joueur.f, Color('#C8AD7F'), (self.r.x,self.r.y), self.r.width/4) # Dessiner le chapeau
        pygame.draw.circle(Joueur.f, Color('#000000'), (self.r.x,self.r.y), self.r.width/4, width=2) # Dessiner le chapeau


class Poulet() :
    """ An object represents a chicken that is animated in a Pygame window.

	The entity is inscribed within the bounding rectangle defined by r. 
        r : pygame.Rect       The encompassing rectangle.
    """

    @staticmethod
    def set_fenetre(fenetre):
        """ Set the class variable f that represents the graphics window.

            window : pygame.Surface
        """
        Poulet.f = fenetre

    def __init__(self, rectangle, nombre_etats, nom_dossier, largeur_fenetre, hauteur_fenetre):
        self.r = rectangle
        self.l = largeur_fenetre
        self.h = hauteur_fenetre
        self.image_animation = []
        self.nombre_etats = nombre_etats
        self.etat_courant = random.randint(1, 32)
        self.prochain_saut = pygame.time.get_ticks() + random.randint(2000, 5000)
        self.direction_x = random.choice(["gauche", "droite"])
        self.direction_y = random.choice(["haut", "bas"])
        for i in range(nombre_etats):
            try:
                chemin_image = f"{nom_dossier}/frame_{i+1}.gif"
                self.image_animation.append(
                    pygame.transform.scale(
                        pygame.image.load(chemin_image), 
                        (self.r.width, self.r.height)
                    )
                )
            except FileNotFoundError:
                raise Moteur.Exceptions.FichierIntrouvableErreur(chemin_image)

    def faire_saut(self):
        """A method to make the chickens jump.
        
        """
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel >= self.prochain_saut:
            Sons.son_poulet_cot.play()
            if self.direction_x == "gauche" :
                self.r.x = self.r.x - random.randint(2, 20)                
            if (self.r.x < 0 and self.direction_x == "gauche") :
                self.direction_x = "droite"
            if self.direction_x == "droite" :
                self.r.x = self.r.x + random.randint(2, 20)
            if (self.r.x > (self.l - self.r.width) and self.direction_x == "droite") :
                self.direction_x = "gauche"
            if self.direction_y == "haut" :
                self.r.y = self.r.y - random.randint(2, 15)                
            if (self.r.y < 0 and self.direction_y == "haut") :
                self.direction_y = "bas"
            if self.direction_y == "bas" :
                self.r.y = self.r.y + random.randint(2, 15)
            if (self.r.y > (self.h - self.r.height) and self.direction_y == "bas") :
                self.direction_y = "haut"                    
            self.prochain_saut = temps_actuel + random.randint(2000, 5000)
        
    def dessiner(self):
        """ Draw a chicken.

	    The chicken is inscribed within the bounding rectangle defined by the object variable r in a Pygame window.
        """
        Poulet.f.blit(self.image_animation[self.etat_courant], [self.r.x, self.r.y])
    
    def prochaine_scene(self):
        """A method that allows updating the animation of the animated GIF of chickens.
        
        """
        self.etat_courant=(self.etat_courant+1)%self.nombre_etats
