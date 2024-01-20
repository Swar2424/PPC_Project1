import tkinter as tk
from tkinter import scrolledtext
import csv
import math
import random


class Fenetre_avec_graphique():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique")
        self.R = 6378.000 # Rayon de la terre en km 

        #création des attributs autour du dictionnaire des sommets
        self.dicoSommets = {} # dico des sommets avec leur position (structure de travail)
        self.seuil = 0.0 
        self.distance_max = 0.0
        self.distance_min = 0.0
        
        # Lecture des données vers le dictionnaire et 
        # positionnement des variables distance_min et distance_max (pour le slider)
        self.fichier = 'villes_extrait.csv'
        self.creer_dico()
        self.distance_min_max()
        
        ########################################
        # Attributs liés à l'affichage graphique
        ########################################
        
        # Dimensions du canevas de dession de la fenêtre d'affichage
        self.f_graph_height = 650
        self.f_graph_width = 650

        # Calcul des coordonnées cartésiennes min et max des villes du dictionnaire 
        # dans le repère d'affichage (nécessaires pour le changement de coordonnées)
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0
        self.calcul_min_max_xy()
        
        # Décalages pour élargir le cadre d'affichage
        self.offset_earth = 100
        self.offset_screen = 50

        # Fenêtre d'affichage contenant le canevas
        self.f_graph = None
        
        self.couleur = ["black", "red", "green", "blue", "yellow", "magenta","cyan", "white", "purple"]
        self.dicoSommetsGraphiques = {} # récupère les id des sommet dessinés sur le canevas
        
        # création des widgets
        self.creer_widgets(self.racine)

    def creer_widgets(self,root):
         """
        crée les widgets de l'application
        :paramètres: root la fenêtre racine
        :return:
        """
       
        # création de la zone scrolledText avec scrall bar dans laquelle les informations seront intégrées
        
        # création des boutons de l'interface

        # création du curseur
                

    def creer_dico(self):
        """
            à compléter
        """

        
    def distance_min_max(self):
        """
            à compléter
        """

        
    def quitter(self, event):
        """
            à compléter
        """
    
        
    def denombre_sommets(self, event):
        """
            à compléter
        """


    def distance_moyenne(self,event):
        """
            à compléter
        """


    def ville_distance_seuil(self, event):
        """
            à compléter
        """

    
  ##########################################################
  ##########################################################
  # Partie graphique : on dessine le graphe des villes 
  ##########################################################
  ##########################################################
  
  ###############################
  ##### Changement de référentiel
  ##### et calcul des distances
  ###############################

    def calcul_min_max_xy(self):
        '''
        
        détermine les coordonnées min et max en y et y des villes dans le plan du canevas
        et met à jour les attributs les représentant en conséquence
        Parameters
        ----------
        None

        Returns
        -------
        None.

        '''
        x_min = math.inf
        x_max = -math.inf
        y_min = math.inf
        y_max = -math.inf
        
        for nom, lat, lng, h in self.dicoSommets.values():
            x_test, y_test = self.xy_from_lat_long(lat, lng)
            if x_test < x_min :
                x_min = x_test
            if x_test > x_max :
                x_max = x_test
            if y_test < y_min :
                y_min = y_test
            if y_test > y_max :
                y_max = y_test

        self.x_min = x_min
        self.x_max = x_max 
        self.y_min = y_min
        self.y_max = y_max
            

    def xy_from_lat_long(self, latitude, longitude):
        '''
        Conversion de la latitude et longitude en coordonnées x-y plan du canevas sans normalisation
        Parameters
        ----------
        latitude : float
            valeur de la latitude en degrés
        longitude : float
            valeur de la longitude en degrés

        Returns
        -------
        x, y: float, float
            valeurs approchées des coordonnées en x et y dans le plan du canevas.

        '''
        longitude = longitude + 180
        x = ((longitude * self.f_graph_width)/360)
        
        latitude = latitude + 90
        hauteur = (latitude * self.f_graph_height)/180 
        y = self.f_graph_height - hauteur
        
        return x, y
    
    
    def xy_repere_cartesien(self, latitude, longitude, offset1, offset2):
        '''
        fonction qui effectue le changement de repère complet de la longitude d'une ville
        à sa position normalisée dans le repère (x,y) du canevas veillant à respecter les bordures

        Parameters
        ----------
        liste_coord : liste 2D représentant les descripteurs de chaque ville(id, nom, lat, long, alt)
        idVille : int
            identifiant de la ville.
        offset1 : int
            décalage assurant un retrait en bordure droite
        offset2 : int
            décalage assurant un retrait en bordure gauche

        Returns
        -------
        x, y : float
            valeurs des coordonnées normalisée dans le plan du canevas

        '''
        x_ville, y_ville = self.xy_from_lat_long(latitude, longitude)
                        
        x = (self.f_graph_width - offset1) / (self.x_max - self.x_min) * (x_ville - self.x_min) + offset2
        y = (self.f_graph_height - offset1) / (self.y_max - self.y_min) * (y_ville - self.y_min) + offset2 
        
        return x, y


  ##############################################
  ### calcul de distance dans le bon référentiel
  ##### du GPS au cartésien
  #### changement de référentiel
  ##############################################

    #Conversion des degrés en radian
    def convertRad(self, val_degre):
        """
        Convertir une valeur passé en degrés en radian
        - val_degre(float): la valeur à conversir en degrés
        Retour:
        - la valeur en radian (float)
        """
        return (math.pi * val_degre) / 180

    def distanceKm(self,lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre):
        """
        Calculer la distance  en km entre deux lieux repérées par leurs coordonnées GPS 
        - lat_a_degre, lon_a_degre, lat_b_degre, lon_b_degre (float): les 4 coordonnées des deux emplacements en degrés (latitude, longitude)
        Retour:
        - la valeur de la distance réelle ramenée à la surface de la terre (valeur approchée) en float
        """
        lat_a = self.convertRad(lat_a_degre)
        lon_a = self.convertRad(lon_a_degre)
        lat_b = self.convertRad(lat_b_degre)
        lon_b = self.convertRad(lon_b_degre)
        distKm = self.R * (math.pi/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))
        return distKm

    def distance (self, x0, y0, x1, y1):
        return math.sqrt ((x1-x0)**2+(y1-y0)**2)        
            
            
  ###################################################################
  # Les fonctions de dessins sont à compléter ici : sommet et arêtes
  ###################################################################
    
            
  ########################################################################
  # La partie d'interaction au clic de souris sur la carte => affiche info
  ########################################################################

     

if __name__ == "__main__":
    app = Fenetre_avec_graphique()
    app.racine.mainloop()
