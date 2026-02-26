"""
    Module that contains the exception classes.
"""

class Erreur(Exception):
    """
        Base class for exceptions in this module.
    """
    pass


class ErreurPygameInitialisation(Erreur):
    """
    An exception is raised if pygame or pygame.mixer fails to initialize.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Erreur d'initialisation Pygame : {self.message}"


class FichierIntrouvableErreur(Erreur):
    """
        Class for exceptions of files not found.
    """
    def __init__(self, nom_fichier):
        self.n = nom_fichier

    def __str__(self):
        return f"Erreur : le fichier '{self.n}' est introuvable."